#!/usr/bin/env python3
import sys, os
from cmd import Cmd
from colorama import Fore, Back, Style


#Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Style: DIM, NORMAL, BRIGHT, RESET_ALL

target=""
fork=False


class MyPrompt(Cmd):
    prompt = "#"
    def do_upload(self, inp):
        pass
 
    def do_download(self, inp):
        pass

    def default(self, inp):
        pass
        
    def do_exit(self, inp):
        global fork
        if fork:
            forkbomb()
        return True
 

def gather_infos():
    log("getting most important information:")
    global target
    pass

def gather_more():
    global target
    gather_infos()
    log("getting more information:")
    pass

def download(path):
    global target
    pass

def upload(path):
    global target
    pass

def forkbomb():
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
