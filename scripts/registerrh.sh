#!/bin/sh

# This script registers a system into Satellite server

os=$(cat /etc/redhat-release)
osver_pos=$(cat /etc/redhat-release | grep -aob release | cut -d: -f1)
release=${os:osver_pos+8:3}

# Clean older registrations
subscription-manager unregister
subscription-manager repos --disable "*"
subscription-manager clean
yum clean all
rm -rf /var/cache/yum/*

# Download and install Satellite's CA certificate
curl --insecure --output katello-ca-consumer-latest.noarch.rpm https://iblstllv01.weizmann.ac.il/pub/katello-ca-consumer-latest.noarch.rpm
yum -y localinstall katello-ca-consumer-latest.noarch.rpm 

# Choosing correct activation key
if [[ "$release" == "8"* ]];   then            
				key="RHEL 8"
elif [[ "$release" == "7"* ]]; then            
				key="RHEL 7"
elif [[ "$release" == "6"* ]]; then            
				key="RHEL 6"
fi

subscription-manager register --force --org="Weizmann_Institute_of_Science" --activationkey="$key"
yum -y install katello-host-tools katello-host-tools-tracer
sed -i 's/proxy_hostname =.*/proxy_hostname =/' /etc/rhsm/rhsm.conf
