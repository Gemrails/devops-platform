#!/usr/bin/python
#coding=utf-8

import read_ini
import logsys
import os

class WriteFile(object):
    def __init__(self, sect, key):
        self.sect = sect
        self.key = key
        self.cf = read_ini.config()
        self.logs = logsys.LogSys()
        pass

    def w_upfile(self, filename, msg):
        updir = self.cf.getvalue(self.sect, self.key)
        if os.path.exists(updir):
            pass
        else:
            try:
                os.mkdir(updir)
            except Exception, e:
                errmsg = "mkdiruppathErr " + str(e)
                self.logs.writelog(errmsg)
        uppath = updir + filename
        if msg :
            try:
                fp = open(uppath, 'w')
                fp.write(msg)
                fp.close()
                return 0
            except Exception, e:
                errmsg = "write upfile Error " + str(e)
                self.logs.writelog(errmsg)
                return 9
        else:
            return 8

    def w_logfile(self, msg):
        # 之前写的有些文件中利用到来原来writefile文件中的write_file方法
        # 现在将这里重新补充到write_file中,之前文件需要利用时记得修改...
        filepath = self.cf.getvalue(self.sect, self.key)
        filedir = ('/').join(filepath.split('/')[:-1])
        if os.path.exists(filedir):
            pass
        else:
            try:
                os.mkdir(filedir)
            except Exception, e:
                errmsg = "mkdirlogpathErr " + str(e)
                self.logs.writelog(errmsg)
        if msg:
            try:
                fp = open(filepath, 'a')
                fp.write(msg)
                fp.close()
                return 0
            except Exception, e:
                print "writeError " + str(e)
                return 9
        else:
            return 8


