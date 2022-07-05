#!/bin/sh

# This script registers a system into Satellite server

os=$(cat /etc/redhat-release)
osver_pos=$(cat /etc/redhat-release | grep -aob release | cut -d: -f1)
release=${os:osver_pos+8:3}

distribution=$(rpm -qf /etc/redhat-release 2> /dev/null | tail -n 1)

# Change os variable to appropriate keyword
if 	 [[ "$distribution" == "redhat"* ]]; then
		os="RHEL"
elif [[ "$distribution" == "centos"* ]]; then
		os="CentOS"
elif [[ "$distribution" == "oraclelinux"* ]]; then
		os="ORACLE"
fi

# Clean older registrations
subscription-manager unregister           2> /dev/null
subscription-manager repos --disable "*"  2> /dev/null
yum-config-manager --disable \*     	  2> /dev/null
sed -i 's/enabled *= *1/enabled=0/g' /etc/yum.repos.d/*.repo
subscription-manager clean				  2> /dev/null
yum clean all
rm -rf /var/cache/yum/*

# Remove Proxy configuration from RHSM and ENV variables
sed -i 's/proxy_hostname =.*/proxy_hostname =/' /etc/rhsm/rhsm.conf
unset http_proxy
unset https_proxy

# Download and install Satellite's CA certificate
curl --insecure --output katello-ca-consumer-latest.noarch.rpm https://"$1"/pub/katello-ca-consumer-latest.noarch.rpm
yum -y localinstall katello-ca-consumer-latest.noarch.rpm 

# Choosing correct activation key
if [[ "$release" == "8"* ]];   then            
				key="$os 8"
elif [[ "$release" == "7"* ]]; then
		if [[ "$(hostname -f)" == "$1" ]]; then
		     	key="Satellite/Capsule"
	    else 	key="$os 7"
		fi
				
elif [[ "$release" == "6"* ]]; then            
				key="RHEL 6"
fi

# Start the activation process
subscription-manager register --force --org="Weizmann_Institute_of_Science" --activationkey="$key"

# Install additional packages for Red-Hat systems
if [[ "$os" == "RHEL" ]]; then
		yum -y install katello-host-tools katello-host-tools-tracer
fi
