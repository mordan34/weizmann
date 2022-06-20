import sys
import json
import ipaddress
import os

def get_env(ip):
        envname = None
        with open('/tmp/satellite.json', 'r') as f:
            satelliteobj=json.load(f)
            f.close()
        for env in satelliteobj["environments"]:
            for subnet in env.get('subnets'):
                if (ipaddress.ip_address(ip) in ipaddress.ip_network(subnet)):
                    envname=env.get('name')           
        return envname
    
# Main routine to Check Network/IP and return the related Environment
if len(sys.argv) == 2:
    env=get_env(sys.argv[1])
    if not env is None:
        env=env.strip("\r\n")
    print(env, sep='', end='')
