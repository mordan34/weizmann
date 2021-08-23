import json
import os
import requests
import socket
import pandas
import certifi

# Global Variables

# Path of the .csv file to extract data from
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + '/data/inventar.csv'

# URI in the API to execute
BASEURL =  "https://ibapvtv01.weizmann.ac.il:8443/api/"
TASK = BASEURL + "runTask"
LOGIN = BASEURL + "login"

POST_HEADERS = {'content-type': 'application/json'}

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
            
# Send Post request to Cyberm8 in order to open ports for our system
def post_json(location, json_data):
        result=requests.post(
            location,
            data=json_data,
            auth=(USERNAME, PASSWORD),
            verify=SSL_VERIFY,
            headers=POST_HEADERS
        )
        return result.json


# Main routine to open rules for specific Server
ip = '10.160.3.28'

#try: 
task_json=load_data(PATH, ip)
login_json={ "username": USERNAME, "password": PASSWORD }
#result=post_json(LOGIN, json.dumps( login_json ) )

with requests.Session() as s:
        s.post(LOGIN, data=login_json)
        r = s.get('https://ibapvtv01.weizmann.ac.il:8443/operator/tasks')
        print(r.content)
#result2=post_json(TASK, json.dumps( task_json ) )
#print(result2)
#print("Created request successfully for IP\t" + ip)

#except:  print("Unable to invoke API request for IP\t" + ip, "\n\nDetails:" + result)
