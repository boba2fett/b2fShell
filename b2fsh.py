#!/usr/bin/env python3
import sys, os
from cmd import Cmd


target=""


class MyPrompt(Cmd):
    prompt = "#"
    def do_upload(self, inp):
        pass
        return True
 
    def do_download(self, inp):
        pass
        return True

    def default(self, inp):
        pass
        return True
 


def main(target, auto: ('extracts the most important information', 'flag', 'a'),full: ('extracts the all important information', 'flag', 'f')):
    "Use with b2fshell.php or b2fshell-headless.php"
    globals()['target'] = target
    globals()['auto'] = auto
    globals()['full'] = full
    MyPrompt().cmdloop()

if __name__ == '__main__':
    import plac; plac.call(main)
