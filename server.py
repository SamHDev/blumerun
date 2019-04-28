import flask
import json
import subprocess
import os
import time
import threading
import signal

cdir = os.path.dirname(__file__)
try:
    os.mkdir(os.path.join(cdir,"log/"))
except FileExistsError:
    pass
logdir = os.path.join(cdir,"log/")

sessions = {}
def load():
    f = open("data.json")
    data = json.loads(f.read())
    f.close()
    for sid in data["instances"].keys():
        sdata = data["instances"][sid]
        session = Instance(sid)
        session.name = sdata["name"]
        session.enabled = sdata["enabled"]
        session.pipe = None
        session.dir = sdata["dir"]
        session.script = sdata["script"]
        session.onstart = sdata["onstart"]
        session.restart = sdata["restart"]
        sessions[sid] = session

        if (session.enabled and session.onstart):
            session.start(by="AUTO-START")
        
def save():
    data= {}
    for sid in sessions.keys():
        session = sessions[sid]
        sdata = {}
        sdata["name"] = session.name
        sdata["enabled"] = session.enabled
        sdata["dir"] = session.dir
        sdata["script"] = session.script
        sdata["onstart"] =session.onstart
        sdata["restart"] =session.restart
        
        data[sid] = sdata
    f = open("data.json","w")
    f.write(json.dumps({"instances":data},indent=4))
    f.close()
      

class Instance():
    def __init__(self,ids):
        self.id = ids
        self.name = None
        self.enabled = None
        self.dir = None
        self.script = None
        self.restart = None
        self.onstart = None
        self.shutdown = False
        
        self.pipe = None
        
    def gets(self):
        logs = os.path.join(logdir,self.id+".txt")
        return logs,"./"+self.script
    def start(self,by="N/A"):
        logs,cmds = self.gets()
        try:
            os.remove(logs)
        except FileNotFoundError:
            pass
        open(logs,"a").write("[STARTED BY "+by+"]\n")
        self.pipe = subprocess.Popen(cmds,cwd=self.dir,shell=True,stdout=open(logs,"a"),stderr=open(logs,"a"),stdin=subprocess.PIPE,preexec_fn=os.setsid)
    def stop(self,by="N/A"):
        logs,cmds = self.gets()
        open(logs,"a").write("[STOPPED BY "+by+"]\n")
        if (self.pipe == None):return
        #self.pipe.terminate()
        os.killpg(os.getpgid(self.pipe.pid), signal.SIGTERM)
    def kill(self):
        logs,cmds = self.gets()
        open(logs,"a").write("[KILLED BY "+by+"]\n")
        if (self.pipe == None):return
        os.killpg(os.getpgid(self.pipe.pid), signal.SIGTERM)
    def poll(self):
        if (self.pipe == None):return False
        return (self.pipe.poll() == None)
    def readConsole(self):
        return open(self.gets()[0],"r").read()
    def writeConsole(self,write):
        return self.pipe.stdin(write+"\n")
     
def monitor():
    time.sleep(30)
    print("Starting Monitor")
    while True:
        time.sleep(10)
        for sk in sessions.keys():
            s = sessions[sk]
            if (s.poll() == False) and (s.restart == True) and (s.enabled == True) and (s.shutdown == False):
                try:
                    s.kill()
                except:
                    pass
                print("Monitor: Restarting " + s.name)
                s.start(by="AUTO-RESTART")
        
        
        
load()        
        
app = flask.Flask(__name__)        

@app.route("/ping",methods=["GET"])
def ping():
    return "pong"

@app.route("/add",methods=["POST"])
def add():
    new_id = flask.request.form.get("id")
    new_name = flask.request.form.get("name")
    new_dir = flask.request.form.get("dir")
    new_script = flask.request.form.get("script")
    
    if (new_id in sessions.keys()):
        return json.dumps({"s":False,"m":"Name Already Exists","d":{},"o":None})
    
    session = Instance(new_id)
    session.name = new_name
    session.enabled = True
    session.pipe = None
    session.dir = new_dir
    session.script = new_script
    session.restart = True
    session.onstart = True
    sessions[new_id] = session
    save()
    
    return json.dumps({"s":True,"m":"Successfuly Added Script " + new_name + " ("+new_id+")","d":{},"o":None})

@app.route("/remove",methods=["POST"])
def remove():
    ids = flask.request.form.get("id")
    if (ids not in sessions.keys()):
        return json.dumps({"s":False,"m":"Name does not Exist","d":{},"o":None})
    sessions[ids].kill()
    names = sessions[ids].name
    del sessions[ids]
    return json.dumps({"s":True,"m":"Successfuly Removed " + names + " ("+ids+")","d":{},"o":None})

@app.route("/list",methods=["GET"])
def list():
    data = []
    for skey in sessions.keys():
        s = sessions[skey]
        sdata = {}
        sdata["id"] = s.id
        sdata["name"] = s.name
        data.append(sdata)
    print(data)
    return json.dumps({"s":True,"m":"","d":{"list":data},"o":None})

@app.route("/get",methods=["GET"])
def get():
    ids = flask.request.args.get("id")
    if (ids not in sessions.keys()):
        return json.dumps({"s":False,"m":"Name does not Exist","d":{},"o":None})
    sdata = {}
    sdata["id"] =sessions[ids].id
    sdata["name"] =sessions[ids].name
    sdata["enabled"] =sessions[ids].enabled
    sdata["dir"] =sessions[ids].dir
    sdata["script"] =sessions[ids].script
    sdata["onstart"] =sessions[ids].onstart
    sdata["restart"] =sessions[ids].restart
    return json.dumps({"s":True,"m":"","d":sdata,"o":None})

@app.route("/edit",methods=["POST"])
def edit():
    ids = flask.request.form.get("id")
    key = flask.request.form.get("key")
    value = flask.request.form.get("value")
    print(ids)
    print(key)
    print(value)
    print(str(type(value)))
    if (ids not in sessions.keys()):
        return json.dumps({"s":False,"m":"Name does not Exist","d":{},"o":None})
    if (key not in ["name","dir","script","onstart","restart"]):
        return json.dumps({"s":False,"m":"Edit Key does not Exist","d":{},"o":None})
    if (key == "onstart"):
        if (type(value) != bool): return json.dumps({"s":False,"m":"Invaild Type","d":{},"o":None})
        sessions[ids].onstart = value
    if (key == "restart"):
        if (type(value) != bool): return json.dumps({"s":False,"m":"Invaild Type","d":{},"o":None})
        sessions[ids].restart = value
    if (key == "dir"):
        if (type(value) != str): return json.dumps({"s":False,"m":"Invaild Type","d":{},"o":None})
        sessions[ids].dir = value
    if (key == "script"):
        if (type(value) != str): return json.dumps({"s":False,"m":"Invaild Type","d":{},"o":None})
        sessions[ids].script = value
    if (key == "name"):
        if (type(value) != str): return json.dumps({"s":False,"m":"Invaild Type","d":{},"o":None})
        sessions[ids].name = value
        
    save()
    return json.dumps({"s":True,"m":"Changed '"+key+"' to '"+value+"' on "+sessions[ids].name,"d":{},"o":None})

@app.route("/enable",methods=["POST"])
def enable():
    ids = flask.request.form.get("id")
    if (ids not in sessions.keys()):
        return json.dumps({"s":False,"m":"Name does not Exist","d":{},"o":None})
    if (sessions[ids].enabled == True):
        return json.dumps({"s":False,"m":sessions[ids].name+" is already Enabled","d":{},"o":None})
    sessions[ids].enabled = True
    save()
    return json.dumps({"s":True,"m":"Enabled '"+sessions[ids].name+"'","d":{},"o":None})

@app.route("/disable",methods=["POST"])
def disable():
    ids = flask.request.form.get("id")
    if (ids not in sessions.keys()):
        return json.dumps({"s":False,"m":"Name does not Exist","d":{},"o":None})
    if (sessions[ids].enabled == False):
        return json.dumps({"s":False,"m":"Script is already Disabled","d":{},"o":None})
    sessions[ids].enabled = False
    save()
    return json.dumps({"s":True,"m":"Disabled '"+sessions[ids].name+"'","d":{},"o":None})

@app.route("/start",methods=["POST"])
def start():
    ids = flask.request.form.get("id")
    if (ids not in sessions.keys()):
        return json.dumps({"s":False,"m":"Name does not Exist","d":{},"o":None})
    if (sessions[ids].poll() == True):
        return json.dumps({"s":False,"m":"Script is already Started","d":{},"o":None})
    sessions[ids].start(by="USER")
    sessions[ids].shutdown = False
    return json.dumps({"s":True,"m":"Starting '"+sessions[ids].name+"'","d":{},"o":None})

@app.route("/stop",methods=["POST"])
def stop():
    ids = flask.request.form.get("id")
    if (ids not in sessions.keys()):
        return json.dumps({"s":False,"m":"Name does not Exist","d":{},"o":None})
    if (sessions[ids].poll() == False):
        return json.dumps({"s":False,"m":"Script is already Stoped","d":{},"o":None})
    sessions[ids].stop(by="USER")
    sessions[ids].shutdown = True
    return json.dumps({"s":True,"m":"Stopping '"+sessions[ids].name+"'","d":{},"o":None})

@app.route("/restart",methods=["POST"])
def restart():
    ids = flask.request.form.get("id")
    if (ids not in sessions.keys()):
        return json.dumps({"s":False,"m":"Name does not Exist","d":{},"o":None})
    if (sessions[ids].poll() == True):
        sessions[ids].stop()
    sessions[ids].start(by="USER")
    sessions[ids].shutdown = False
    return json.dumps({"s":True,"m":"Restarted '"+sessions[ids].name+"'","d":{},"o":None})

@app.route("/kill",methods=["POST"])
def kill():
    ids = flask.request.form.get("id")
    if (ids not in sessions.keys()):
        return json.dumps({"s":False,"m":"Name does not Exist","d":{},"o":None})
    if (sessions[ids].poll() == True):
        return json.dumps({"s":False,"m":"Script is already Stopped","d":{},"o":None})
    sessions[ids].kill()
    sessions[ids].shutdown = True
    return json.dumps({"s":True,"m":"Killing script '"+sessions[ids].name+"'","d":{},"o":None})

@app.route("/status",methods=["GET"])
def status():
    ids = flask.request.args.get("id")
    if (ids not in sessions.keys()):
        return json.dumps({"s":False,"m":"Name does not Exist","d":{},"o":None})
    return json.dumps({"s":True,"m":"","d":{"name":sessions[ids].name,"running":sessions[ids].poll()},"o":None})

@app.route("/console/read",methods=["GET"])
def console_read():
    ids = flask.request.args.get("id")
    if (ids not in sessions.keys()):
        return json.dumps({"s":False,"m":"Name does not Exist","d":{},"o":None})
    return json.dumps({"s":True,"m":"","d":{"data":sessions[ids].readConsole(),"name":sessions[ids].name},"o":None})

@app.route("/console/write",methods=["POST"])
def console_write():
    ids = flask.request.form.get("id")
    cmd = flask.request.form.get("cmd")
    print(cmd)
    if (ids not in sessions.keys()):
        return json.dumps({"s":False,"m":"Name does not Exist","d":{},"o":None})
    sessions[ids].writeConsole(cmd)
    return json.dumps({"s":True,"m":"","d":{"cmd":cmd,"name":sessions[ids].name},"o":None})

thd = threading.Thread(target=monitor,daemon=True)
thd.start()

app.run(port=8640)
