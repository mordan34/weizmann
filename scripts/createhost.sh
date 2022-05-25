#!/bin/bash

server="iblstllv01.weizmann.ac.il"

# Create host from image on the VC
hammer  --server https://$server --username admin host create --name $1 --hostgroup "DC_HostGroup_RHEL8" --provision-method 'image' --enabled true --managed true --compute-profile-id 2 --image "RHEL8-DC-tmpl" --puppet-environment-id 3 --architecture-id 1 --domain-id 1  --puppet-proxy-id 1 --location-id 2 --organization-id 1 --build 1 --interface "managed=true,primary=true,provision=true,compute_type=VirtualVmxnet3,compute_network=VLAN78_DC_MOM,type=interface,domain_id=1,identifier=ens192,subnet_id=22" &

# Waiting for the host creation to finish
pid=$!
wait $pid
name="$1"'.weizmann.ac.il'


# Start the host immediatly after creation
hammer host start --name $name

