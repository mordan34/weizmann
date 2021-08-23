import json
import os
import requests
import socket
import pandas

# Path of the .csv file to extract data from
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + '/data/inventar.csv'
LOCATION = "https://ibapvtv01.weizmann.ac.il:8443/api/runTask"

# Building the task for a specific system
def get_json(record):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + '/templates/cyberm8.json') as json_file:
        data = json.load(json_file)
        tasks=[ (sub) for sub in data['item']]
        task=json.dumps(tasks[1]['request']['body']['raw'], indent=4)
        task=task.replace("Server Name",record["Name"])
        task=task.replace("Server Description",record["Description"])
        task=task.replace("Server Owner",record["Systemowner"])
        task=task.replace("System Name",record["Name"])
        task=task.replace("1.8.8.7",record["Ip"])
        task=task.replace("Requestor",record["ContactPerson"])
        return task

# Extract relevant data from a row in our .csv file
def load_data(PATH, ip):
        inventar = pandas.read_csv(PATH)
        inv=inventar.set_index("Ip", drop = False)
        record=inv.loc[ip, :]
        print(get_json(record))
            
# Send Post request to Cyberm8 in order to open ports for our system
def post_json(location, json_obj):
        result=requests.post(
            location=LOCATION,
            data=json_obj
        )

ip = '10.150.10.29'
load_data(PATH, ip)