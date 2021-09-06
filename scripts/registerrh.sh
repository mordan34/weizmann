#!/bin/sh


# This script registers a system into Satellite server



os=$(cat /etc/redhat-release)
osver_pos=$(cat /etc/redhat-release | grep -aob release | cut -d: -f1)
release=${os:osver_pos+8:3}

# Download and install Satellite's CA certificate
curl --insecure --output katello-ca-consumer-latest.noarch.rpm https://iblstlv01.weizmann.ac.il/pub/katello-ca-consumer-latest.noarch.rpm
yum -y localinstall katello-ca-consumer-latest.noarch.rpm 

# Choosing correct activation key
if [ $release == "8*" ];   then            key="RHEL $release"
elif [ $release == "7*" ]; then            key="RHEL 7"

subscription-manager register --org="Weizmann_Institute_of_Science" --activationkey=$key
subscription-manager release --set=$release
yum -y install katello-host-tools
yum -y install katello-host-tools-tracer
yum -y install katello-agent

#curl -O https://iblstlv01.weizmann.ac.il/pub/bootstrap.py
#chmod +x bootstrap.py
#/usr/libexec/platform-python bootstrap.py --login=admin --server iblstlv01.weizmann.ac.il --release=$release --location="Weizmann Lan" --organization="Weizmann_Institute_of_Science" --hostgroup="VXRail_VC" --activationkey=Dev --force --download-method https --skip 'foreman' --install-katello-agent
