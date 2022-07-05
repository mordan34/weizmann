import json
import os
import requests
import socket
import sys
import ipaddress
import ssl
import certifi
from requests.structures import CaseInsensitiveDict

# Global Variables

# API Task Json string with initial details
PAYLOAD_Test='{"task_id":"62af06eb3e167a1b8f44d4cb","parameters":{"environment":"DCTest","type":"Linux","server_name":"hostname","server_description":"Satellite Provisioned host","server_owner":"mordan","system_name":"hostname","ip_address":"IP","requestor":"mordan"}}'
NEW_SERVER='{"task_id":"621bea3d3e167a0908c58c53","parameters":{"environment":"DCTest","type":"Linux","server_name":"hostname","server_description":"Satellite Provisioned host","server_owner":"mordan","system_name":"hostname","ip_address":"IP","requestor":"mordan"}}'

# URI in the API to execute
BASEURL =  "https://ibapvtv01.weizmann.ac.il:8443"
TASKURL = BASEURL + "/api/runTask"
LOGINURL = BASEURL + "/api/login"

POST_HEADERS = CaseInsensitiveDict()
POST_HEADERS["Accept"] = "application/json"
POST_HEADERS["Content-Type"] = "application/json"

# Credentials to login to Cyberm8 retrieved from Ansible Tower
USERNAME = os.environ.get("username")
PASSWORD = os.environ.get("password")
# Ignore SSL
SSL_VERIFY = True

# This function is used to update the json object with the correct hostname and it's IP
def update_data(hostname):
        try:
            ip = socket.gethostbyname(hostname)
            jsonObj = json.loads(NEW_SERVER)
            jsonObj['parameters']['server_name'] =        hostname
            jsonObj['parameters']['system_name'] =        hostname
            jsonObj['parameters']['ip_address'] =         ip
            jsonObj['parameters']['environment'] =        get_env(ip)
            jsonObj['parameters']['server_description'] = os.environ.get("description")
            jsonObj['parameters']['requestor'] =          os.environ.get("requestor")
        except: 
            jsonObj = None
            print("Unable to gather information for\t" + hostname)
        return json.dumps(jsonObj)
    
# This function returns the environment to which the server belongs to (DC / DMZ / DMZTest / DCTest)
def get_env(ip):
        with open('../playbooks/inventory/group_vars/satellite.json',"r") as f:
            satelliteobj=json.load(f)
        for env in satelliteobj["environments"]:
            envname=env.get('name')
            for subnet in env.get('subnets'):
                if (ipaddress.ip_address(ip) in ipaddress.ip_network(subnet)):
                    return envname
        sys.exit(1)

# Main routine to open rules for specific Server
if len(sys.argv) == 2:
    hostname = sys.argv[1] 
    login_json = { "username": USERNAME, "password": PASSWORD }
    task_json = update_data(hostname)

    if ( task_json != None ):
        with requests.Session() as s:
                response = s.post(LOGINURL, json=login_json, headers=POST_HEADERS, verify='cyberm8.pem')
                POST_HEADERS["Authorization"]=response.headers['Authorization']
                response = s.post(TASKURL, data=task_json, headers=POST_HEADERS, verify='cyberm8.pem')

                if ( response.status_code == 200 ):
                        print("Created request successfully for server\t" + hostname)
                else:  
                       print("\nUnable to invoke API request for server\t" + hostname + "\n\nDetails:" + str(response))
                       sys.exit(1)

else: print("Fatal Error! Missing hostname paramter for script execution")

