#!/usr/bin/python
from salt import client
from os.path import *
import psutil
import re
import sys
import shutil
import time

class Passport():
    client = client.LocalClient()
    date = time.strftime("%Y%m%d%H", time.localtime())
    def web_host(self):
        host = self.client.cmd('putaoweb-0-189','test.ping')  
        return host
    def web_check(self,hostname):
        nets = self.client.cmd(hostname,'cmd.run',['netstat -antup|grep nginx'])
        return nets
    
    def stop_nginx(self,hostname):
        e = self.client.cmd(hostname, 'file.file_exists', ['/etc/nginx/sites-enabled/passport.putao.io.conf'])
        d = self.client.cmd(hostname, 'file.directory_exists', ['/data/deploy/nginx'])
        s = (e[hostname])
        f = (d[hostname])
        if s is True:
            if f is True:
                c = self.client.cmd(hostname, 'cmd.run', ['mv /etc/nginx/sites-enabled/passport.putao.io.conf /data/deploy/nginx/'])
                r = (c[hostname])
                if r is not True:
                    reload = self.client.cmd(hostname,'cmd.run',['/etc/init.d/nginx reload'])
                    return reload
            else:
                m = self.client.cmd(hostname, 'file.mkdir', ['/data/deploy/nginx'])
                c = self.client.cmd(hostname, 'cmd.run', ['mv /etc/nginx/sites-enabled/passport.putao.io.conf /data/deploy/nginx'])
                r = (c[hostname])
                if r is not True:
                    reload = self.client.cmd(hostname,'cmd.run',['/etc/init.d/nginx reload'])
                    return reload
        else:
            return None
 
    def start_nginx(self,hostname):
        e = self.client.cmd(hostname, 'file.file_exists', ['/etc/nginx/sites-enabled/passport.putao.io.conf'])
        s = (e[hostname])
        if s is not True:
            c = self.client.cmd(hostname, 'cmd.run', ['mv /data/deploy/nginx/passport.putao.io.conf /etc/nginx/sites-enabled'])
            r = (c[hostname])
            if r is not True:
                reload = self.client.cmd(hostname,'cmd.run',['/etc/init.d/nginx reload'])
                return reload
        else:                                                             
            return None
    
    def gzip_pro(self,hostname):
        e = self.client.cmd(hostname,'file.directory_exists',['/data/web/passport.putao.io'])
        r = (e[hostname])
        if r is not False:
            gzip = self.client.cmd(hostname, 'archive.zip',['/data/deploy/passport.putao.io_%s.zip' % self.date,'/data/web/passport.putao.io'])
            delt = self.client.cmd(hostname,'file.rename',['/data/web/passport.putao.io','/data/deploy/passport.putao.io-%s' % self.date])
            return gzip
            return delt
        else:
            print '/data/web/passport.putao.io is not exist!'

    def web_pro(self,hostname):
        get_dir = self.client.cmd(hostname,'cp.get_dir',['salt://web_pro/passport.putao.io','/data/web/'])
        return get_dir


def main():
    p = Passport()
    for i in p.web_host():
        yield [re.search('80',(p.web_check(i))[i]),i]
if __name__ == '__main__':
    main()
    for i in main():
        if i[0] is not None:
            print "port of %s web server is open:" % i[1],  i[0].group()
            stop = Passport().stop_nginx(i[1])
            if stop is not None:
                print 'backup configure file is success,mv command retuen null value'      
                print '\033[5;32;40m'                                                   
                print '***reload*** %s nginx already reload' % i[1]   
                print '\033[0m'                                                         
                
                print '\033[5;32;40m'   
                print 'web procedure gzip and delete old procedure!!!!'
                print '\033[0m'
                Passport().gzip_pro(i[1])

                pro = Passport().web_pro(i[1])
                for f in (pro[i[1]]):
                    print f

                print '\033[5;32;40m'

                print "%s transfer's file amount is:" % i[1], len(pro[i[1]])
                print '\033[0m'

                if True:
                    Passport().start_nginx(i[1])
                    print 'recover configure file is file sucess,mv command return null value'
                    print '\033[5;32;40m'                                                 
                    print "****reload sucess*** %s nginx already reaload,Please check passport.putao.com whever Ok!!"
                    print '\033[0m'                                                       
            else:
                print '\033[1;31;40m'                 
                print "/salt/test.php maybe not exsits. Please check!! thanks!" 
                print '\033[0m'                       

        else:
            print '\033[1;31;40m'
            print "ERROR: Port of %s web server is close,Please check!!!!" % i[1]
            print '\033[0m'
