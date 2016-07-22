#!/usr/bin/python
#coding=utf-8

from lib.conn_redis import CRedis
from lib.read_ini import config
from logsys import LogSys
from UpWeb import ExcuteConn  #ExcuteConn中含有统一远程调用的方法
import os
from lib.thread_pool import ThreadPool
import time

class ExcuteErrLog(object):

    def __init__(self):
        self.rf = config()
        self.thp = ThreadPool()
        self.log = LogSys()
        self.cr = CRedis()
        pass

    def __getconf(self, sect, key):

        return self.rf.getvalue(sect, key)
        pass

    def __choosemodule(self, value):
        print value
        result={
            1 : self.__getconf('logpath_conf', 'ecg_errlog'),
            2 : self.__getconf('logpath_conf', 'run_errlog'),
            3 : self.__getconf('logpath_conf', 'doctor_errlog'),
            4 : self.__getconf('logpath_conf', 'ecg_dblog'),
            5 : self.__getconf('logpath_conf', 'run_dblog'),
            6 : self.__getconf('logpath_conf', 'doctor_dblog'),
            7 : self.__getconf('logpath_conf', 'web_errlog'),
            8 : self.__getconf('logpath_conf', 'web_dblog'),
            9 : self.__getconf('logpath_conf', 'mysqllog')
        }
        print result.get(value)
        return result.get(value)

    def __timet(self):
        TIMEFORMAT = '%Y/%m/%d'                # Y 2016年  y 16年
        nowtime = time.strftime(TIMEFORMAT, time.localtime())
        return nowtime

    def showcount(self, logcont):
        _count = 0
        _dex = 0
        _rdex = 0
        _listcont = []
        ttime = self.__timet()
        for line in logcont:
            _dex += 1
            if ttime in line:
                if _count == 0:
                    _rdex = _dex
                _count += 1
        if _rdex:
            _listcont =  logcont[(_rdex-1):]
        _listcont.append(_count)
        return _listcont

    def getpinlog(self, dev, num):
        _rc = 0
        time.sleep(0.1)
        filepath = self.__choosemodule(num)
        ec = ExcuteConn(dev, 1)
        key = "%s%s" %(dev, num)
        comm = 'cat %s' % str(filepath)
        comm1 = 'cat %s' % (str(filepath) + ".1")
        print comm
        print comm1
        rc1 = ec.allexcute(comm)
        rc2 = ec.allexcute(comm1)
        if rc2 != 0 and rc1 != 0 :
            logcont = (rc2 + rc1)
        elif rc1 != 0:
            logcont =  rc1
        else:
            logcont = []
        print logcont
        listcont = self.showcount(logcont)
        listcont.append(len(listcont))
        if listcont:
            for mm in listcont:
                #rc = self.cr.pipline(key, mm)
                # 封装额pipeline方法有问题= =
                _rc = self.cr.rrpush(key, mm)
            # self.cr.llrange(key, (-int(self.cr.llrange(key, -1, -1)[0])), -1)
            # 在列表中最后写入最后一次插入这个列表的长度
            return _rc
        else:
            return 9

    def geterrnum(self, dev, num):
        newkey = "lognum"
        okey = "%s%s" %(dev, num)
        if self.cr.iexist(okey):
            value = self.cr.llrange(okey, -2, -2)[0]
        else:
            value = '0'
        newvalue = "%s%s-%s" %(dev, num, value)
        self.cr.rrpush(newkey,newvalue)
        pass

    def getmain(self, dev, num):
        #print "%s" %(dev)
        time.sleep(0.1)
        print "%s-%s" %(dev, num)

    def threadexcu(self):
        serverlist = ['web_m', 'web_b', 'web_s']
        for dev in serverlist:
            for i in range(1, 9):
                self.thp.creatappend(self.getpinlog, [dev, i])
        self.thp.thgo()

    def insertnum(self):
        self.cr.remove("lognum")
        serverlist = ['web_m', 'web_b', 'web_s']
        for dev in serverlist:
            for i in range(1, 9):
                self.thp.creatappend(self.geterrnum, [dev, i])
        self.thp.thgo()

    def getnum(self):
        nl = (',').join(self.cr.llrange("lognum", 0, -1))
        return nl

    def getlog(self, key):
        if self.cr.iexist(key) and int(self.cr.llrange(key, -2, -2)[0]):
            log = ('^.').join(self.cr.llrange(key, (-int(self.cr.llrange(key, -1, -1)[0])), -3))
        else:
            log = "No log."
            #log = ('@').join(self.cr.llrange('test1141', -33, -4))
        return log

    def sendmail(self, mail):
        fbash = self.__getconf('script_path', 'sendlogmail')
        commd = "%s %s" %(fbash, mail)
        ec = ExcuteConn('support', 0)
        ec.allexcute(commd)
        return 0

if __name__== '__main__':
    el = ExcuteErrLog()
    #el.getpinlog('test114', '1')
    #el.threadexcu()
    #el.threadnum()
    #el.getnum()
