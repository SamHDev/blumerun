#!/bin/sh

version() { echo "$@" | awk -F. '{ printf("%d%03d%03d%03d\n", $1,$2,$3,$4); }'; }

DATAE=`wget -q -O - "https://raw.githubusercontent.com/SamHDev/blumerun/master/version.txt"`
DATAC=`cat /usr/local/blumerun/version.txt`

if [ $(version $DATAC) -ge $(version $DATAE) ]; then
    echo "Already Up to Date"
    exit 3
fi

sudo wget https://raw.githubusercontent.com/SamHDev/blumerun/master/updater.sh -P /usr/local/blumerun
sudo chmod 777 /usr/local/blumerun/updater.sh
sudo bash /usr/local/blumerun/updater.sh
sudo rm /usr/local/blumerun/updater.sh

systemctl restart blumerun
echo "Updated to $DATAE"
