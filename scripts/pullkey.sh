#!/bin/bash


mkdir ~/.ssh
curl https://iblstlv01.weizmann.ac.il:9090/ssh/pubkey >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
