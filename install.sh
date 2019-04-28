#!/bin/sh
#PREP INSTALLER
echo BlumeRun Installer
echo ----------------------------------------
mkdir /usr/local/blumerun
mkdir /usr/local/blumerun/bin
mkdir /usr/local/blumerun/log
sudo apt-get install wget
#INSTALL FILES
echo Installing Files
wget https://raw.githubusercontent.com/SamHDev/blumerun/master/server.py -P /usr/local/blumerun
wget https://raw.githubusercontent.com/SamHDev/blumerun/master/start-server.sh -P /usr/local/blumerun
wget https://raw.githubusercontent.com/SamHDev/blumerun/master/client.py -P /usr/local/blumerun
wget https://raw.githubusercontent.com/SamHDev/blumerun/master/data.json -P /usr/local/blumerun
wget https://raw.githubusercontent.com/SamHDev/blumerun/master/blumerun -P /usr/local/blumerun/bin
wget https://raw.githubusercontent.com/SamHDev/blumerun/master/blumerun.service  -P /usr/local/blumerun.service
#DEBUG
mv /usr/local/blumerun/bin/blumerun /usr/local/blumerun/bin/blumerun2
#PERM FIX
echo Fixing Permsions
chmod 777 /usr/local/blumerun/start-server.sh
chmod 777 /usr/local/blumerun/bin/blumerun2
#SERVICE CREATE
echo Creating Service
mv /usr/local/blumerun/blumerun.service /etc/systemd/system/blumerun2.service
systemctl daemon-reload
systemctl enable blumerun2
systemctl start blumerun2
#APTH
echo Adding to Path
echo 'export PATH="/usr/local/blumerun/bin:$PATH"\n' >> ~/.bashrc
export PATH="/usr/local/blumerun/bin:$PATH"
#END MSG
echo Done
echo ----------------------------------------
echo "\nTo Get started run: blumerun help"
