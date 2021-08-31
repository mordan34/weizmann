#!/bin/bash

server="iblstlv01.weizmann.ac.il"

# Create host from image on the VC
hammer  --server https://$server --username admin host create --name $1 --hostgroup "VXRail_VC" --compute-profile-id 2 --image "RHEL-8-64-LAN" --partition-table-id 109 --medium-id 12 --puppet-environment-id 1 --architecture-id 1 --domain-id 1  --puppet-proxy-id 1 --location-id 2 --organization-id 1 --mac "$(facter macaddress)" --build 1 &

# Waiting for the host creation to finish
pid=$!
wait $pid
name="$1"'.weizmann.ac.il'


# Start the host immediatly after creation
hammer host start --name $name

