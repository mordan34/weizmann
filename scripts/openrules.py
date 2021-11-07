import json
import os
import requests
import socket
import sys
from requests.structures import CaseInsensitiveDict

# Global Variables

# API Task Json string with initial details
PAYLOAD='{"task_id":"610bd0b33e167a0b0c87f176","parameters":{"environment":"DCTest","type":"Linux","server_name":"hostname","server_description":"Satellite Provisioned host","server_owner":"mordan","system_name":"hostname","ip_address":"IP","requestor":"Mor Danino"}}'

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
SSL_VERIFY = False


def update_data(hostname):
        try:
            ip = socket.gethostbyname(hostname+".weizmann.ac.il")
            jsonObj = json.loads(PAYLOAD)
            jsonObj['parameters']['server_name'] = hostname
            jsonObj['parameters']['system_name'] = hostname
            jsonObj['parameters']['ip_address'] = ip
        except: 
            jsonObj = None
            print("Unable to find IP address for\t" + hostname)
        return json.dumps(jsonObj)

# Main routine to open rules for specific Server
if len(sys.argv) == 2:
    hostname = sys.argv[1] 
    login_json = { "username": USERNAME, "password": PASSWORD }
    task_json = update_data(hostname)

    if ( task_json != None ):
        with requests.Session() as s:
                response = s.post(LOGINURL, json=login_json, headers=POST_HEADERS)
                POST_HEADERS["Authorization"]=response.headers['Authorization']
                response = s.post(TASKURL, data=task_json, headers=POST_HEADERS)

                if ( response.status_code == 200 ):
                        print("Created request successfully for server\t" + hostname)
                else:  print("\nUnable to invoke API request for server\t" + hostname + "\n\nDetails:" + str(response))

else: print("Fatal Error! Missing hostname paramter for script execution")

