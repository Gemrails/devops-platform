#!/usr/bin/python
#coding=utf-8

import dealwith_http_log as dwlog
import lib.read_ini as read_ini
import sys
import time

INIFILE = '/Users/pujielan/Documents/code/web_upload/auto_config.ini'

def __init__(ttime):

    readcf = read_ini.config(INIFILE)
    try:
        everypath = readcf.getvalue('logpath_conf', 'nginx_status')
        #print everypath
    except Exception, e:
        print "getpath Error!" + str(e)
        return 9

    nginxtime = dwlog.TransTime()
    nginxstatus = dwlog.NginxStatus(nginxtime.nginx_time(ttime), everypath)
    nginxstatus.ipnums()
    time.sleep(0.5)
    nginxstatus.hot_urls(20)
    time.sleep(0.5)
    nginxstatus.increase_500(5)
    time.sleep(0.5)
    nginxstatus.hot_time(20)
    time.sleep(0.5)
    #nginxstatus.get_urlstatus('http://ecg.mhealth365.cn:9900/nginx_status')


if __name__ == '__main__':

    if len(sys.argv) == 2 and len(sys.argv[1]) == 8:
        __init__(str(sys.argv[1]))
        #__init__("20160201")
    else:
        print "\nNeed argv likes 20150708.\n"
    #if len(sys.argv) == 2 and len(sys.argv[1]) == 8:
    #    __init__(sys.argv[1])
    #else:
    #    print "\nNeed argv likes 20150710.\n"
