import json
import os
import requests
import socket
import pandas
import certifi
import sys
from requests.structures import CaseInsensitiveDict

# Global Variables

# Path of the .csv file to extract data from
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + '/data/inventar.csv'

# API Task Json string with initial details
PAYLOAD="{\r\n\t\"task_id\": \"610bd0b33e167a0b0c87f176\",\r\n\t\"parameters\": {\r\n\t\t\"environment\": \"DCTest\",\r\n\t\t\"type\": \"Linux\",\r\n\t\t\"server_name\": \"hostname\",\r\n\t\t\"server_description\": \"Satellite Provisioned host\",\r\n\t\t\"server_owner\": \"MORDAN\",\r\n\t\t\"system_name\": \"hostname\",\r\n\t\t\"ip_address\": \"10.160.3.28\",\r\n\t\t\"requestor\": \"Mor Danino\"\r\n\t}\r\n}"

# URI in the API to execute
BASEURL =  "https://ibapvtv01.weizmann.ac.il:8443"
TASKURL = BASEURL + "/api/runTask"
LOGINURL = BASEURL + "/api/login"

POST_HEADERS = CaseInsensitiveDict()
POST_HEADERS["Accept"] = "application/json"
POST_HEADERS["Content-Type"] = "application/json"

# Default credentials to login to Satellite 6
USERNAME = "ansibletest"
PASSWORD = "jvUFjUzkR7rM7Qdq"
# Ignore SSL
SSL_VERIFY = False


# Building the task for a specific system
def get_json(record):
    if ( record["Status"] == 'Test' ):
            env='DCTest'
    elif (record["Status"] == 'Prod' ):   
            env='DC'
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + '/templates/cyberm8.json') as json_file:
        data = json.load(json_file)
        tasks=[ (sub) for sub in data['item']]
        task=json.dumps(tasks[1]['request']['body']['raw'], indent=4)
        task=task.replace("DC",env)
        task=task.replace("Server Name",record["Name"])
        task=task.replace("Server Description",record["Description"])
        task=task.replace("Server Owner",record["Systemowner"])
        task=task.replace("System Name",record["Name"])
        task=task.replace("1.8.8.7",record["Ip"])
        task=task.replace("Requestor",record["ContactPerson"])
        data['item'][1]['request']['body']['raw']=task
        return data

# Extract relevant data from a row in our .csv file and returns json
def load_data(PATH, ip):
        inventar = pandas.read_csv(PATH)
        inv=inventar.set_index("Ip", drop = False)
        record=inv.loc[ip, :]
        return ( get_json(record) )

def update_data(hostname):
        ip = socket.gethostbyname(hostname+".weizmann.ac.il")
        return PAYLOAD

# Main routine to open rules for specific Server
print(sys.argv[1])
if len(sys.argv) == 2:
    hostname = sys.argv[1] 
    login_json = { "username": USERNAME, "password": PASSWORD }
    task_json = update_data(hostname)

    with requests.Session() as s:
        response = s.post(LOGINURL, json=login_json, headers=POST_HEADERS)
        POST_HEADERS["Authorization"]=response.headers['Authorization']
        response = s.post(TASKURL, data=task_json, headers=POST_HEADERS)
        
        if ( response.status_code == 200 ):
                print("Created request successfully for server\t" + hostname)
        else:  print("Unable to invoke API request for server\t" + hostname, "\n\nDetails:" + response.content)

else: print("Fatal Error! Missing hostname paramter for script execution")

