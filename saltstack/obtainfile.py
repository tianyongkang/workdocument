#!/usr/bin/env python
import os
import sys
import time


def obtain_file():
    date = time.strftime("%Y%m%d%H%M", time.localtime())
    fname = '/salt/python/upload'
    f = file(fname,'r')
    fr = f.read().split()
    f1 = []

    for f in fr:
        try:
            if os.path.exists(f):
                f2 = f
            f1 += [f2]
        except UnboundLocalError,e:
            f1 = []
    return f1
