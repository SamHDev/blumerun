#!/bin/sh

rm /usr/local/blumerun/version.txt
wget https://raw.githubusercontent.com/SamHDev/blumerun/master/version.txt -P /usr/local/blumerun

rm /usr/local/blumerun/server.py
wget https://raw.githubusercontent.com/SamHDev/blumerun/master/server.py -P /usr/local/blumerun
rm /usr/local/blumerun/client.py
wget https://raw.githubusercontent.com/SamHDev/blumerun/master/client.py -P /usr/local/blumerun
rm /usr/local/blumerun/update.sh
wget https://raw.githubusercontent.com/SamHDev/blumerun/master/update.sh -P /usr/local/blumerun
rm /usr/local/blumerun/uninstall.sh
wget https://raw.githubusercontent.com/SamHDev/blumerun/master/uninstall.sh -P /usr/local/blumerun

chmod 777 /usr/local/blumerun/uninstall.sh
chmod 777 /usr/local/blumerun/update.sh
