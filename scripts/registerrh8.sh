#!/bin/sh


# This script registers a system into Satellite server

curl -O https://iblstlv01.weizmann.ac.il/pub/bootstrap.py

chmod +x bootstrap.py

os=$(cat /etc/redhat-release)
osver_pos=$(cat /etc/redhat-release | grep -aob release | cut -d: -f1)
release=${os:osver_pos+8:3}

/usr/libexec/platform-python bootstrap.py --login=mordan --server iblstlv01.weizmann.ac.il --release=$release --location="Weizmann Lan" --organization="Weizmann_Institute_of_Science" --hostgroup="Dev_RHEL8_VC" --activationkey=Dev --force --download-method https --skip foreman --install-katello-agent
