#!/bin/sh

version() { echo "$@" | awk -F. '{ printf("%d%03d%03d%03d\n", $1,$2,$3,$4); }'; }

DATAE=`curl -s "https://raw.githubusercontent.com/SamHDev/blumerun/master/version.txt"`
DATAC=`cat version.txt`

if [ $(version $DATAC) -ge $(version $DATAE) ]; then
    echo "Already Up to Date"
    exit 3
fi

wget -q https://raw.githubusercontent.com/SamHDev/blumerun/master/updater.sh -P /usr/local/blumerun
chmod 777 /usr/local/blumerun/updater.sh
/usr/local/blumerun/updater.sh
rm /usr/local/blumerun/updater.sh
echo "Updated to $DATAE"
