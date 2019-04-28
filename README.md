# blumerun
A Custom Script Executor &amp; Service Runner for Ubuntu

## Install
```bash
sudo apt-get install wget
wget https://raw.githubusercontent.com/SamHDev/blumerun/master/install.sh
chmod 777 install.sh
./install.sh
rm install.sh
```
## Uninstall
```bash
/usr/local/blumerun/uninstall.sh
```

## Usage
### Add a Script
All scripts are run from a bash file, regardless if they are python or java.
You first need to create a .sh file to run your code. 
In this example I'm running a simple python script
```py
import time
count = 0
while True:
    print("LOOP! (",count,")")
    time.sleep(1)
    count = count + 1
```
