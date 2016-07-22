#/usr/bin/python
#coding=utf-8

import dealwith_http_log
import lib.read_ini as read_ini
import logsys
import lib.conn_redis as connredis
import time
import datetime

log = logsys.LogSys()

def __setconf(confpath, kind):
    readcf = read_ini.config(dealwith_http_log.INIFILE)
    try:
        everypath = readcf.getvalue(confpath, kind)
    except Exception, e:
        errstr = "getpath Error!<__setconf>" + str(e)
        log.writelog(errstr)
    return everypath

'''
def switch_func(kind):
    # 在下面的字典当中会直接执行每个值当中的函数,所以,会出现那种实例化之后立刻被调用的假象.
    inistr = __InitString()
    result={
        'index_num1'    : inistr.func_index_num1(),
        'index_num2'    : inistr.func_index_num2(),
        'index_num3'    : inistr.func_index_num3(),
        'index_num4'    : inistr.func_index_num4(),
        'index_line'    : inistr.func_index_line(),
        'index_o'       : inistr.func_index_o(),
        'index_ecg'     : inistr.func_index_ecg(),
        'index_run'     : inistr.func_index_run(),
        'tables'        : inistr.func_tables(),
        'charts'        : inistr.func_charts()
    }
    return inistr
'''
def switch_func(kind):

    if "num" in kind:
        return switch_num(kind)
    elif "line" in kind:
        return switch_line()
    elif "index_o" in kind:
        return switch_index_o()
    elif "index_ecg" in kind:
        return switch_indexecg()
    elif "index_run" in kind:
        return switch_indexrun()
    else:
        pass

    pass

def switch_indexecg():
    inistr = __InitString()
    postr = "index_tb:%s" % inistr.func_indexecg()
    return postr

def switch_indexrun():
    inistr = __InitString()
    postr = "index_tb:%s" % inistr.func_indexrun()
    return postr

def switch_num(kind):
    inistr = __InitString()
    return "num:%s" % inistr.func_index_num(kind)

def switch_line():
    date0 = int(time.mktime(time.strptime(datetime.datetime.now().strftime("%Y-%m-%d"),"%Y-%m-%d")))
    inistr = __InitString()
    str = inistr.func_index_line()
    postr = ("line:%d=" + str) % date0
    return postr

def switch_index_o():
    inistr = __InitString()
    str = "index_o:%s" % inistr.func_index_o()
    return str
    pass

class __InitString(object):

    def __init__(self):
        self.cnredis = connredis.CRedis()

    def func_index_num(self, kind):
        mm = self.cnredis.get(kind)
        return mm

    def func_index_line(self):
        key = 'index_line'
        mm = self.cnredis.llrange(key, '0', '-1')
        strmm = ','.join(mm)
        return strmm
        pass

    def func_index_o(self):
        key = 'index_o'
        mm = self.cnredis.llrange(key, '0', '-1')
        strmm = ','.join(mm)
        return strmm
        pass

    def func_indexecg(self):
        key = 'index_ecg'
        mm = self.cnredis.llrange(key, '0', '-1')
        if len(mm)>10:
            strmm = ','.join(mm[0:9])
            print strmm
            return strmm
        pass

    def func_indexrun(self):
        key = 'index_run'
        mm = self.cnredis.llrange(key, '0', '-1')
        strmm = ','.join(mm)
        return strmm
        pass

    def func_tables(self):
        pass

    def func_charts(self):

        pass


if __name__=='__main__':

    switch_func('num')
