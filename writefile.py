#/usr/bin/python
#coding=utf-8

import lib.read_ini as read_ini
import os
import sys
import logsys

class WritePath(object):

    def __init__(self, inipath):

        readcf = read_ini.config(inipath)
        self.pathin = readcf.getvalue('write_path', 'pathin')
        filepath = ('/').join(self.pathin.split('/')[:-1])
        if os.path.exists(filepath):
            pass
        else:
            os.mkdir(filepath)
        pass

    def write_file(self, comm):
        try:
            fp = open(self.pathin, 'a')
            fp.write(comm)
            fp.close()
        except Exception, e:
            print "writeError " + str(e)
            return 9
        pass
