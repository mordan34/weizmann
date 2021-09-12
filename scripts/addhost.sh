#!/bin/bash

server="iblstlv01.weizmann.ac.il"

hammer  --server https://$server --username admin host create --name $1  --enabled true --managed true --puppet-environment-id 3 --architecture-id 1 --domain-id 1  --puppet-proxy-id 1 --operatingsystem-id 3 --partition-table-id 7 --location-id 2 --organization-id 1 --medium-id 12 --build 0 --hostgroup "VXRail_VC" &

pid=$!
wait $pid
name="$1"'.weizmann.ac.il'

hammer host start --name $name
