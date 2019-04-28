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
In this example I'm running a simple python script called `looptest.py`
```py
import time
count = 0
while True:
    print("LOOP! (",count,")")
    time.sleep(1)
    count = count + 1
```
Then I create a .sh file to run this named `looptest.sh`
```bash
python3 -u loop.py
```
The `-u` argument for the python flushes all output from `print` commands allowing blumerun the see the output
All we need to do next is add the script. We can run
```bash
blumerun add looptest
```
This should enter us into a wizard. Fill in the prompts like this example
```
root@server:~/blumerun add looptest
Add Session Wizard:
        Description Name[Looptest]: Loop Demo
        Working Directory[/root/]:
        Script File[looptest.sh]:
Successfuly Added Script Loop Demo (looptest)
```
And done, its that simple, and it starts automagicly
### Start/Stop/Restart a script
*(Replace `looptest` with the id you added your script with)*

To Start a stop script, simply run:
```
blumerun start looptest
```
Or to stop a script
```
blumerun stop looptest
```
