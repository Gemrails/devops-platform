#!/usr/bin/python
#coding=utf-8

import dealwith_http_log
import lib.read_ini as read_ini
import logsys

log = logsys.LogSys()

def __setconf(confpath, kind):
    readcf = read_ini.config(dealwith_http_log.INIFILE)
    try:
        everypath = readcf.getvalue(confpath, kind)
    except Exception, e:
        errstr = "getpath Error!<__setconf>" + str(e)
        log.writelog(errstr)
    return everypath

def nginxpost(strs,nums = 20):
     # 将改为从数据库读取数据,目前的写法仅用做调试使用,因此处理大文件会稍微慢一些
    try:
        datetime = strs.split('&')[0].split('=')[1]
    except Exception, e:
        errstr = "datatime Error!<nginxpost>" + str(e)
        log.writelog(errstr)
    #datetime = strs
    nginxstatus = dealwith_http_log.NginxStatus(dealwith_http_log.TransTime().nginx_time(datetime), __setconf('logpath_conf', 'nginx_status'))

    ipnums = "ip数量为: %d" %(nginxstatus.ipnums())
    hottime = nginxstatus.hot_time(nums).split('\n')
        #nginxstatus.hot_time(10)
        #nginxstatus.hot_urls(10)
    #print hottime
    return hottime
    pass

def getone(gdata):
    # 处理从浏览器post过来的字符串
    value1 = gdata.split('&')[0].split('=')[1]
    return value1
    pass


if __name__ == '__main__':
    nginxpost("20160312")
