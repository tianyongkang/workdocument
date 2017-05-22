#!/usr/bin/python
from salt import client
from os.path import *
import psutil
import re
import sys
import shutil
import time

class Update():
    client = client.LocalClient()
    date = time.strftime("%Y%m%d%H%M", time.localtime())
    d1 = sys.argv[1]
    d2 = sys.argv[2]
    def web_host(self):
        host = self.client.cmd('groupweb','cmd.run',['hostname'],expr_form='nodegroup') 
        return host

    def zip_dir(self,hostname):
        e = self.client.cmd(hostname, 'file.directory_exists', [self.d2])
        e1 = (e[hostname])
        if e1 is True:
            gzip = self.client.cmd(hostname, 'archive.zip', ['/data/deploy/%s_%s.zip' % (self.d1,self.date),'%s/%s' % (self.d2, self.d1)])
            print '%s/%s' % (self.d2,self.d1),'gzip to /data/deploy Success!!!!!!'
            rn = self.client.cmd(hostname, 'file.rename', ['%s/%s' % (self.d2,self.d1), '/salt/%s-%s' % (self.d1, self.date)])
            print '%s/%s',(self.d2,self.d1),'mv file Sucess,Please Update file',rn
        else:
            print self.d2,'is not exist!'
    def copy_file(self,hostname):
        f = self.client.cmd(hostname, 'file.file_exists',['%s/%s' % (self.d2,self.d1)])                        
        f1 = (f[hostname])
        if f1 is True:
            cpfile = self.client.cmd(hostname, 'file.copy', ['%s/%s' % (self.d2,self.d1), '/data/deploy/%s_%s' % (self.d1, self.date)])
            print '%s/%s' % (self.d2,self.d1),'cpoy to /data/deploy Sucess',cpfile
        else:
            print '%s/%s' %(self.d2,self.d1),'is not exist!'
    def update_dir(self,hostname):
        dir = self.client.cmd(hostname, 'cp.get_dir', ['salt://web_conf/%s' % self.d1, self.d2])
        for i in dir:
            print i
            for i1 in (dir[i]):
                print i1

    def update_file(self,hostname):
        file = self.client.cmd(hostname, 'cp.get_file', ['salt://web_conf/%s' % self.d1, '%s/%s' % (self.d2,self.d1)])
        print file

def main():
    p = Update()
    for i in p.web_host():
        if isdir('/salt/web_conf/%s' % sys.argv[1]):
            p.zip_dir(i)
            p.update_dir(i)

        elif isfile('/salt/web_conf/%s' % sys.argv[1]):
            p.copy_file(i)
            p.update_file(i)
        else:
            print '%s file not a file or dirctory!!!' % sys.argv[1]


if __name__ == '__main__':
    main()
