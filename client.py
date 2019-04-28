version = open("/usr/local/blumerun/version.txt").read()

import sys
import os
import requests
import threading
import time
import tty

args = sys.argv
args.pop(0)
if (len(args) == 0):
    print("""BlumeRun
    Version: {ver}
    Made by: SamHDev
        """.format(ver=version))
    sys.exit(0)
if args[0] == "help":
    resp = """
    BlumeRun Help:
       {cmd}list - Lists all scripts
       {cmd}add <id> - Add a new script
       {cmd}remove <id> - Remove a script
       {cmd}edit <id> - Edit a script
       {cmd}enable <id> - Enable a disabled script
       {cmd}disable <id> - Disable a script
       {cmd}start <id> Start a script
       {cmd}stop <id> - Stop a script
       {cmd}restart <id> - Restart a script
       {cmd}kill <id> - Force Kill a script
       {cmd}status <id> See if a script is running
       {cmd}output <id> - Retreive output for a script
       {cmd}console <id> - Open a console Session with a script
       {cmd}execute <id> <input> - Enter in text into the script
       {cmd}help - Print Help
       {cmd}reload - Reload BlumeRun (Restart All Scripts)
       {cmd}update - Run a Version Check and update BlumeRun
    """
    print(resp.format(cmd="blumerun "))
    sys.exit(0)

if args[0] == "ping":    
    r = requests.get("http://localhost:8640/ping")
    print(r.text.title()+"!")
    sys.exit(0)
if args[0] == "reload":
    if (input("Are you sure you want to reload all scripts? [Y/N] ").strip().lower() not in ["y","yes"]):
        print("Cancelled")
        sys.exit(0)
    else:
        os.system("systemctl restart blumerun")
        sys.exit(0)
if args[0] == "update":
    if (input("Are you sure you want to update? [Y/N] ").strip().lower() not in ["y","yes"]):
        print("Cancelled")
        sys.exit(0)
    else:
        os.system("./update.sh")
        sys.exit(0)
if args[0] == "uninstall":
    if (input("Are you sure you want to uninstall? [Y/N] ").strip().lower() not in ["y","yes"]):
        print("Cancelled")
        sys.exit(0)
    else:
        os.system("./uninstall.sh")
        sys.exit(0)
    
if args[0] == "list" or args[0] == "ls":
    try:
        r = requests.get("http://localhost:8640/list")
        if (r.json()["s"] == True):
            print("Current Scripts:")
            if (len(r.json()["d"]["list"])==0):
                print("\tNo Scripts Found")
                sys.exit(0)
            else:
                for ins in r.json()["d"]["list"]:
                    print("\t"+ins["id"]+" - "+ins["name"])
        else:
            print("ERROR:"+r.json()["m"])
    except requests.exceptions.ConnectionError:
        print("ERROR:Failed to Connect to Deamon")
    sys.exit(0)
if args[0] == "add":
    #Add Command
    
    #Check Command Length
    if (len(args) == 0):
        print("Usage: blumerun add <id>")
        sys.exit(0)
    if (len(args) != 2):
        print("Usage: blumerun add <id>")
        sys.exit(0)
    #Get ID
    ids = args[1]
    print("Add Session Wizard:")
    
    #NAME
    name = input("\tDescription Name["+ids.title()+"]: ")
    if (name == ""):
        name = ids.title()
    
    #Working DIR
    while True:
        cwd = input("\tWorking Directory["+os.getcwd()+"/]: ")
        if (cwd == ""):
            cwd = os.getcwd()+"/"
        if (os.path.exists(cwd) == True):
            break
        print("ERROR:Path does not Exist")
    
    #Script FILE
    while True:
        script = input("\tScript File["+ids+".sh]: ")
        if (script == ""):
            script = ids+".sh"
        if (os.path.exists(os.path.join(cwd,script)) == True):
            break
        print("ERROR:File does not Exist")
    os.system("chmod 777 "+os.path.join(cwd,script))
        
    #Add Request
    try:
        r = requests.post("http://localhost:8640/add",data={"id":ids,"name":name,"dir":cwd,"script":script})
        if (r.json()["s"] == True):
            print(r.json()["m"])
        else:
            print("ERROR:"+r.json()["m"])
    except requests.exceptions.ConnectionError:
        print("ERROR:Failed to Connect to Deamon")
    sys.exit(0)
    
if args[0] == "remove":
    if (len(args) == 0):
        print("Usage: blumerun remove <id>")
        sys.exit(0)
    if (len(args) != 2):
        print("Usage: blumerun remove <id>")
        sys.exit(0)
    #Remove Command  
    ids = args[1]
    if (input("Are you sure you want to remove script '"+ids+"'? [Y/N] ").strip().lower() not in ["y","yes"]):
        print("Cancelled")
        sys.exit(0)
        
    try:
        r = requests.post("http://localhost:8640/remove",data={"id":ids})
        if (r.json()["s"] == True):
            print(r.json()["m"])
        else:
            print("ERROR:"+r.json()["m"])
    except requests.exceptions.ConnectionError:
        print("ERROR:Failed to Connect to Deamon")
    sys.exit(0)
    
if args[0] == "edit":
    if (len(args) == 0):
        print("Usage: blumerun edit <id> <name|dir|script|restart|onstart> <value|true|false>")
        sys.exit(0)
    if (len(args) < 4):
        print("Usage: blumerun edit <id> <name|dir|script|restart|onstart> <value|true|false>")
        sys.exit(0)
    #Remove Command  
    ids = args[1]
    key = args[2]
    value = " ".join(args[3:])
        
    if (key not in ["name","dir","script","restart","onstart"]):
        print("Usage: blumerun edit <id> <name|dir|script|restart|onstart> <value|true|false>")
        sys.exit(0)
    if (key in ["restart","onstart"]):
        if (value == "true"):
            value = True
        elif (value == "false"):
            value = False
        else:
            print("Usage: blumerun edit <id> <name|dir|script|restart|onstart> <value|true|false>")
            sys.exit(0)
    try:
        r = requests.post("http://localhost:8640/edit",data={"id":ids,"key":key,"value":value})
        if (r.json()["s"] == True):
            print(r.json()["m"])
        else:
            print("ERROR:"+r.json()["m"])
    except requests.exceptions.ConnectionError:
        print("ERROR:Failed to Connect to Deamon")
    sys.exit(0)   
    
        
if args[0] == "enable":
    if (len(args) == 0):
        print("Usage: blumerun enable <id>")
        sys.exit(0)
    if (len(args) != 2):
        print("Usage: blumerun enable <id>")
        sys.exit(0)
    #Remove Command  
    ids = args[1]
        
    try:
        r = requests.post("http://localhost:8640/enable",data={"id":ids})
        if (r.json()["s"] == True):
            print(r.json()["m"])
        else:
            print("ERROR:"+r.json()["m"])
    except requests.exceptions.ConnectionError:
        print("ERROR:Failed to Connect to Deamon")
    sys.exit(0)    
if args[0] == "disable":
    if (len(args) == 0):
        print("Usage: blumerun disable <id>")
        sys.exit(0)
    if (len(args) != 2):
        print("Usage: blumerun disable <id>")
        sys.exit(0)
    #Remove Command  
    ids = args[1]
        
    try:
        r = requests.post("http://localhost:8640/disable",data={"id":ids})
        if (r.json()["s"] == True):
            print(r.json()["m"])
        else:
            print("ERROR:"+r.json()["m"])
    except requests.exceptions.ConnectionError:
        print("ERROR:Failed to Connect to Deamon")
    sys.exit(0)    
    
    
if args[0] == "start":
    if (len(args) == 0):
        print("Usage: blumerun start <id>")
        sys.exit(0)
    if (len(args) != 2):
        print("Usage: blumerun start <id>")
        sys.exit(0)
    #Remove Command  
    ids = args[1]
        
    try:
        r = requests.post("http://localhost:8640/start",data={"id":ids})
        if (r.json()["s"] == True):
            print(r.json()["m"])
        else:
            print("ERROR:"+r.json()["m"])
    except requests.exceptions.ConnectionError:
        print("ERROR:Failed to Connect to Deamon")
    sys.exit(0)   
if args[0] == "stop":
    if (len(args) == 0):
        print("Usage: blumerun stop <id>")
        sys.exit(0)
    if (len(args) != 2):
        print("Usage: blumerun stop <id>")
        sys.exit(0)
    #Remove Command  
    ids = args[1]
        
    try:
        r = requests.post("http://localhost:8640/stop",data={"id":ids})
        if (r.json()["s"] == True):
            print(r.json()["m"])
        else:
            print("ERROR:"+r.json()["m"])
    except requests.exceptions.ConnectionError:
        print("ERROR:Failed to Connect to Deamon")
    sys.exit(0)   
    
if args[0] == "restart":
    if (len(args) == 0):
        print("Usage: blumerun restart <id>")
        sys.exit(0)
    if (len(args) != 2):
        print("Usage: blumerun restart <id>")
        sys.exit(0)
    #Remove Command  
    ids = args[1]
        
    try:
        r = requests.post("http://localhost:8640/restart",data={"id":ids})
        if (r.json()["s"] == True):
            print(r.json()["m"])
        else:
            print("ERROR:"+r.json()["m"])
    except requests.exceptions.ConnectionError:
        print("ERROR:Failed to Connect to Deamon")
    sys.exit(0)   
    
    
if args[0] == "status":
    if (len(args) == 0):
        print("Usage: blumerun status <id>")
        sys.exit(0)
    if (len(args) != 2):
        print("Usage: blumerun status <id>")
        sys.exit(0)
    #Remove Command  
    ids = args[1]
        
    try:
        r = requests.get("http://localhost:8640/status",params={"id":ids})
        if (r.json()["s"] == True):
            if (r.json()["d"]["running"] == True):
                print(r.json()["d"]["name"]+": " + "\u001b[1m\u001b[32m"+"Running"+"\u001b[0m")
            else:
                print(r.json()["d"]["name"]+": " + "\u001b[1m\u001b[31m"+"Stopped"+"\u001b[0m")
        else:
            print("ERROR:"+r.json()["m"])
    except requests.exceptions.ConnectionError:
        print("ERROR:Failed to Connect to Deamon")
    sys.exit(0)  
    
if args[0] == "output":
    if (len(args) == 0):
        print("Usage: blumerun output <id>")
        sys.exit(0)
    if (len(args) != 2):
        print("Usage: blumerun output <id>")
        sys.exit(0)
    #Remove Command  
    ids = args[1]
        
    try:
        r = requests.get("http://localhost:8640/console/read",params={"id":ids})
        if (r.json()["s"] == True):
            print("\n\u001b[1m"+r.json()["d"]["name"]+": Output"+"\u001b[0m\n"+("-"*50))
            print("\n".join(r.json()["d"]["data"].split("\n")[-255:]))
            print(""+("-"*50))
        else:
            print("ERROR:"+r.json()["m"])
    except requests.exceptions.ConnectionError:
        print("ERROR:Failed to Connect to Deamon")
    sys.exit(0)
if args[0] == "execute":
    print("ERROR: I WANT TO NO OXYGEN")
    sys.exit(0)
if args[0] == "console":
    if (len(args) == 0):
        print("Usage: blumerun console <id>")
        sys.exit(0)
    if (len(args) != 2):
        print("Usage: blumerun console <id>")
        sys.exit(0)
    #Remove Command  
    ids = args[1]
    
    cx = 100
    cy = 30
    sys.stdout.write("Launching Console Session")
    sys.stdout.flush()
    for i in range(0,10):
        time.sleep(0.1)
        sys.stdout.write(".")
        sys.stdout.flush()
    sys.stdout.write("\u001b[100D")
    data = requests.get("http://localhost:8640/status",params={"id":ids}).json()["d"]
    name = data["name"]
    if (data["running"] != True):
        sys.stdout.write("Failed to Launch Console: "+ name + " is not running\n")
        sys.stdout.flush()
        sys.exit(0)
    sys.stdout.write((" "*50)+"\n")
    sys.stdout.write("\u001b[1m"+name+": Console"+"\u001b[0m\n")
    sys.stdout.flush()
    
    #sys.stdout.write(((("#"*(cx+4))+"\n")*(cy+4)))
    #sys.stdout.write(str("\u001b["+str(2)+"A"))
    sys.stdout.write(("-"*cx)+"\n")
    sys.stdout.write("\n"*(cy-1))
    sys.stdout.write(("-"*cx)+"\n")
    sys.stdout.write(str("\u001b["+str(1)+"A"))
    opens = True
    #tty.setraw(sys.stdin)
    import select
    ltime = time.time()-2
    try:
        while opens:
            while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                #line = sys.stdin.readline()
                line = None
                if line:
                    requests.post("http://localhost:8640/console/write",data={"id":ids,"cmd":line})
                    sys.stdout.write("\u001b[100D")
                    sys.stdout.write(str("\u001b[1A"))
                    sys.stdout.flush()
                else: 
                    pass
            else:
                if (time.time() >= ltime):
                    data = requests.get("http://localhost:8640/console/read",params={"id":ids}).json()["d"]["data"]
                    datatrim = "\n".join(data.split("\n")[-cy:])
                    ltime = time.time()+0.5

                    #sys.stdout.write(str("\u001b["+str(cy+1)+"A"))
                    ##sys.stdout.write((((" "*(cx))+"\n")*(cy)))

                    ##sys.stdout.write(str("\u001b["+str(cy)+"A"))
                    ##sys.stdout.write("\n"*((cy+1)-len(datatrim.split("\n"))))
                    ##sys.stdout.write("## "+str(datatrim).replace("\n","\n## ")[::-1].replace("\n## "[::-1],"",1)[::-1])
                    ##sys.stdout.flush()

                    sys.stdout.write(str("\u001b["+str(cy)+"A"))
                    sys.stdout.write("\n")
                    for i in range(0,cy-1):
                        sys.stdout.write(str("\u001b[2K \n"))
                    sys.stdout.write(str("\u001b["+str(cy)+"A"))
                    sys.stdout.write("\n"*((cy+1)-len(datatrim.split("\n"))))
                    sys.stdout.write(str(datatrim))
    except KeyboardInterrupt:
        sys.stdout.write("\u001b[1B")
        #sys.stdout.write(str("u001b[100D"))
        for i in range(0,cy+3):
            sys.stdout.write(str("\u001b[1A"))
            sys.stdout.write(str("\u001b[2K"))
            #sys.stdout.write(str("u001b[100D"))
        sys.stdout.write(str("\u001b[100D"))
        print("Closed Console Session ("+name+")")
        sys.exit(0)
                
if (True):
    print("Invalid Argument:\nRun: 'blumerun help' to see commands")
