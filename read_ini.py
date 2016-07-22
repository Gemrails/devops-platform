#/usr/bin/python
#coding=utf-8

import ConfigParser
import os

class config():

    def __init__(self, confpath = "/opt/tttt/plat/auto_config.ini"):

        """

        :rtype: object
        """
        self.confpath = confpath
        if os.path.exists(self.confpath):
            pass
        else:
            errmsg = "Confpath isn't in right path!!"
            print errmsg
            # 以后将这里改为一个raise的异常触发来作为提示

        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.confpath)

        if 1 == 0:
            sect = self.cf.sections()
            print "sections:", sect

            logpath = self.cf.options('logpath_conf')    # 此处需要使用单引号
            print "option:", logpath

            nums = self.cf.getint('logpath_conf')        # 获取整数格式

            paths = self.cf.items('logpath_conf')
            print "items:", paths[1][1]

    def getvalue(self, sect, key):

        print self.cf.get(sect, key)
        return self.cf.get(sect, key)


def write_in(filepath, sect, key, value):

    keynum = raw_input("Input Ur keynum:")
    if int(keynum) == 123456:                       # 此处以后用来分配权限管理
        pass
    else:
        print "\n** U have no permission to add config! **"
        return 9
    try:
        cf = ConfigParser.ConfigParser()
        cf.read(filepath)
        cf.set(sect, key, value)
        cf.write(open(filepath,'w'))
    except Exception, e:
        print "write_in:" + str(e)
        return 9
        pass




