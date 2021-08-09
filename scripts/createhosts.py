#!/usr/bin/python

import json
from os import name
import sys
import os.path

try:
    import requests
except ImportError:
    print("Please install the python-requests module.")
    sys.exit(-1)

# URL to your Satellite 6 server
URL = "https://iblstlv01.weizmann.ac.il"
# URL for the API to your deployed Satellite 6 server
SAT_API = "%s/api/v2/" % URL
POST_HEADERS = {'content-type': 'application/json'}
# Default credentials to login to Satellite 6
USERNAME = "admin"
PASSWORD = "ya4HeEhkAjhsdbzs"
# Ignore SSL for now
SSL_VERIFY = False

# Name of the organization to be either created or used
ORG_NAME = "Weizmann Institute of Science"
# Name for hosts to be either created or used
my_file = open(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) + '/data/testhosts')
content = my_file.read()
IMPHOSTS = content.split("\n")
print(IMPHOSTS)

def get_json(location):
    """
    Performs a GET using the passed URL location
    """

    r = requests.get(location, auth=(USERNAME, PASSWORD), verify=SSL_VERIFY)

    return r.json()


def post_json(location, json_data):
    """
    Performs a POST and passes the data to the URL location
    """

    result = requests.post(
        location,
        data=json_data,
        auth=(USERNAME, PASSWORD),
        verify=SSL_VERIFY,
        headers=POST_HEADERS)

    return result.json()


def main():
    """
    Main routine that creates or re-uses an organization and
    life cycle environments. If life cycle environments already
    exist, exit out.
    """

    # Check if our organization already exists
    org = get_json(SAT_API + "organizations/" + ORG_NAME)

    # If our organization is not found, create it
    if org.get('error', None):
        org_id = post_json(
            SAT_API + "organizations/",
            json.dumps({"name": ORG_NAME}))["id"]
        print("Creating organization: \t" + ORG_NAME)
    else:
        # Our organization exists, so let's grab it
        org_id = org['id']
        print("Organization '%s' exists." % ORG_NAME)

    # Now, let's fetch all available hosts for this org...
    hosts = get_json(
        SAT_API + "hosts/")


    # Create a list of existing hosts in Satellite
    hostlist= []
    json_str=json.dumps(hosts['results'], indent=4)
    existinghosts=json.loads(json_str)
    hostlist=  [ (sub['name'].split('.',1))[0] for sub in existinghosts]

    # Create a list of all newly added hosts
    newhosts= []
    for host in IMPHOSTS:
        if ( host not in hostlist):
            newhosts.append(host)

    

if __name__ == "__main__":
    main()