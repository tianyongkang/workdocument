#!/usr/bin/env python

from salt import client    
from os.path import *      
import psutil              
import re                  
import sys                 
import shutil              
import time
from obtainfile import obtain_file

client = client.LocalClient()
date = time.strftime("%Y%m%d", time.localtime())
time = time.strftime("%H%M%S", time.localtime())
web_host = client.cmd('groupweb','test.ping',expr_form='nodegroup')
#web_host = client.cmd('*','test.ping')

class Webupdate():
    def judge_file(self,hn,fname):
        f = client.cmd(hn,'file.file_exists',[fname])
        t = (f[hn])
        if t is not True:
            k = fname.split('/')
            del k[-1]
            v = '/'.join(k)
            d = client.cmd(hn,'file.directory_exists',[v])
            i = (d[hn])
            if i is not True:
                mk = client.cmd(hn, 'file.mkdir', [v])
        return 0

    def judge_dir(self,hn,fname):
        d = client.cmd(hn, 'file.directory_exists',[fname])
        t = (d[hn])
        if t is not True:
            k = fname.split('/')
            del k[-1]
            v = '/'.join(k)
            d = client.cmd(hn,'file.directory_exists', [v])
            i = (d[hn])
            if i is not True:
                mk = client.cmd(hn, 'file.mkdir', [v])
        return 0
    
    def dir_create(self,hn):
        d = client.cmd(hn, 'file.directory_exists', ['/data/deploy/%s' % date])
        t = (d[hn])
        if t is not True:
            client.cmd(hn, 'file.mkdir',['data/deploy/%s' % date])

    def get_file(self,hn, fname):
        f = client.cmd(hn, 'file.file_exists',[fname])
        t = (f[hn])
        if t is True:
            k = fname.split('/')
            fi = k[-1]
            client.cmd(hn,'file.rename',[fname,'/data/deploy/%s/%s' % (date,fi+'-'+time)])
        c = client.cmd(hn, 'cp.get_file', ['salt:/%s' % fname, fname])
        print c

    def get_dir(self,hn, fname):
        f = client.cmd(hn, 'file.directory_exists',[fname])
        t = (f[hn])
        if t is True:
            k = fname.split('/')
            fi = k[-1]
            client.cmd(hn,'file.rename',[fname,'/data/deploy/%s/%s' % (date,fi+'-'+time)])
        fn = fname.split('/')
        del fn[-1]
        v = '/'.join(fn)
        c = client.cmd(hn, 'cp.get_dir', ['salt:/%s' % fname, v])
        print c

def main():
    p = Webupdate()
    if len(obtain_file()) != 0:
        def go():
            for f in obtain_file():
                if isfile(f):
                    for h in web_host:
                        p.judge_file(h,f)
                elif isdir(f):
                    for h in web_host:
                        p.judge_dir(h,f)
            return 0
    else:
        print 'Not file update,Please /data/salt/python/upload!'
    
    if go() == 0:
        for h in web_host:
            p.dir_create(h)
        
        for f in obtain_file():
            if isfile(f):
                for h in web_host:
                    p.get_file(h,f)
            if isdir(f):
                for h in web_host:
                    p.get_dir(h,f)


if __name__ == '__main__':
    main()
