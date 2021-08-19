import json
import os

with open(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + '/templates/cyberm8.json') as json_file:
    data = json.load(json_file)
    tasks=[ (sub) for sub in data['item']]
    task=json.dumps(tasks[1]['request']['body']['raw'], indent=4)
    task=task.replace("Server Name","ibltestv01")
    task=task.replace("Server Description","Test server for python script")
    task=task.replace("Server Owner","Mor Danino")
    task=task.replace("System Name","Python3.9.2")
    task=task.replace("1.8.8.7","127.0.0.1")
    task=task.replace("Requestor","Mor Danino")
    print(task)
