#!/bin/sh
#PREP INSTALLER
echo BlumeRun Installer
echo ----------------------------------------
mkdir /usr/local/blumerun
mkdir /usr/local/blumerun/bin
mkdir /usr/local/blumerun/log
#INSTALL DEPS
echo Getting Dependancies
sudo apt-get install wget -y -qq
echo "  -WGET"
sudo apt-get install python3 -y -qq
echo "  -Python3"
sudo apt-get install python3-pip -y -qq
echo "  -Pip3"
python3 -m pip install flask --quiet
echo "  -Flask"
python3 -m pip install requests --quiet
echo "  -Requests"
#INSTALL FILES
echo "Downoading Files"
wget -q --no-cache https://raw.githubusercontent.com/SamHDev/blumerun/master/server.py -P /usr/local/blumerun
echo "  -Server"
wget -q --no-cache https://raw.githubusercontent.com/SamHDev/blumerun/master/start-server.sh -P /usr/local/blumerun
echo "  -Server Start"
wget -q --no-cache https://raw.githubusercontent.com/SamHDev/blumerun/master/client.py -P /usr/local/blumerun
echo "  -Client"
wget -q --no-cache https://raw.githubusercontent.com/SamHDev/blumerun/master/data.json -P /usr/local/blumerun
echo "  -Data Template"
wget -q --no-cache https://raw.githubusercontent.com/SamHDev/blumerun/master/blumerun -P /usr/local/blumerun/bin
echo "  -Executable"
wget -q --no-cache https://raw.githubusercontent.com/SamHDev/blumerun/master/blumerun.service  -P /usr/local/blumerun
echo "  -Service"
wget -q --no-cache https://raw.githubusercontent.com/SamHDev/blumerun/master/uninstall.sh  -P /usr/local/blumerun
echo "  -Uninstaller"
wget -q --no-cache https://raw.githubusercontent.com/SamHDev/blumerun/master/update.sh  -P /usr/local/blumerun
echo "  -Updater"
wget -q --no-cache https://raw.githubusercontent.com/SamHDev/blumerun/master/version.txt -P /usr/local/blumerun
echo "  -Version Data"
#DEBUG
#mv /usr/local/blumerun/bin/blumerun /usr/local/blumerun/bin/blumerun2
#PERM FIX
echo Writing Permissions
chmod 777 /usr/local/blumerun/uninstall.sh
chmod 777 /usr/local/blumerun/update.sh
chmod 777 /usr/local/blumerun/start-server.sh
chmod 777 /usr/local/blumerun/bin/blumerun
#SERVICE CREATE
echo Creating Service
mv /usr/local/blumerun/blumerun.service /etc/systemd/system/blumerun.service
systemctl daemon-reload
systemctl enable blumerun
echo "  -Starting Service"
systemctl start blumerun
#APTH
echo Adding to Path
echo 'export PATH="/usr/local/blumerun/bin:$PATH"\n' >> ~/.bashrc
echo "  -bashrc Path"
echo '\nPATH=$PATH:/usr/local/blumerun/bin\n' >> ~/etc/profile
echo "  -global Path"
export PATH="/usr/local/blumerun/bin:$PATH"
echo "  -console Path"
#END MSG
echo Done
echo ----------------------------------------
echo "To Get started run: blumerun help"
