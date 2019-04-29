# blumerun
A Custom Script Executor &amp; Service Runner for Ubuntu

## Install
```bash
sudo apt-get install wget
sudo wget https://raw.githubusercontent.com/SamHDev/blumerun/master/install.sh
sudo chmod 777 install.sh
sudo bash install.sh
sudo rm install.sh
```
or as one quick copy paste solution:
```bash
sudo apt-get install wget;sudo wget https://raw.githubusercontent.com/SamHDev/blumerun/master/install.sh;sudo chmod 777 install.sh;sudo bash install.sh;sudo rm install.sh
```

## Update
```bash
blumerun update
```
or if there is an issue:
```bash
sudo bash /usr/local/blumerun/update.sh
```

## Uninstall
```bash
blumerun uninstall
```
or
```bash
sudo bash /usr/local/blumerun/uninstall.sh
```

## Usage
### Add a Script
All scripts are run from a bash file, regardless if they are python or java.
You first need to create a .sh file to run your code. 
In this example I'm running a simple python script called `looptest.py` here is a quick demo script:
```py
import time
count = 0
while True:
    print("LOOP! (",count,")")
    time.sleep(1)
    count = count + 1
```
Then I create a .sh file to run this named `looptest.sh` inside is the command to execute the python script:
```bash
#!/bin/sh
python3 -u loop.py
```
The `-u` argument for the python flushes all output from `print` commands allowing blumerun the see the output
All we need to do next is add the script. We can run
```bash
blumerun add looptest
```
This should enter us into a wizard. Fill in the prompts like this example
```
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
And to restart the script
```
blumerun restart looptest
```
We can see if the script is running by using
```
blumerun status looptest
```

### View a script's output
*(Replace `looptest` with the id you added your script with)*

To Get a quick snapshot of your programs latest output you can run:
```
blumerun output looptest
```
This should print out the last 260 lines

To see a constantly updating version, you can launch a console session by running:
```
blumerun console looptest
```
You can press CTRL+C to exit this.


### View a script's output
*(Replace `looptest` with the id you added your script with)*
We can edit certian feature of a script using the `blumerun edit` command

| Key       | Example Value   | Desc                   |
| --------- |-----------------| -----------------------|
| name      | right-aligned   | $1600                  |
| dir       | centered        |   $12                  |
| script    | are neat        |    $1                  |
| onstart   | are neat        |    $1                  |
| restart   | are neat        |    $1                  |

