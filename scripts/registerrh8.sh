#!/bin/bash


# This script registers a system into Satellite server

curl -O http://iblstlv01.weizmann.ac.il/pub/bootstrap.py

chmod +x bootstrap.py

/usr/libexec/platform-python bootstrap.py --login=mordan --server iblstlv01.weizmann.ac.il --location="Weizmann Lan" --organization="Weizmann Institute of Science" --hostgroup="Dev_RHEL8_VC" --activationkey=Dev --force --download-method https --skip foreman