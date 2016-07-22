#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys
import sqlite3
import time,datetime
from UpWeb import ExcuteConn

now_dir = os.path.split(os.path.realpath(__file__))[0]

#def getLog(bashfile):
#    file = os.popen("bash "+bashfile)
#    logList = file.read().strip('\n').split(',')
#    return logList

def excute_s():
    '''执行远程脚本

    :return: api 字符串
    '''
    command1 = 'bash /phpstudy/server/nginx/logs/AccessLogAnalytics.sh'
    ec = ExcuteConn('nanjingslave', 1)
    rc = ec.allexcute(command1)
    return rc[0].split(',')[6], rc[0].split(',')[7]


def oprApi(apistr):
    ''' 处理api字符串

    :param apistr: api 字符串
    :return: 返回列名和对应值
    '''
    apilist = apistr.split()
    column = ''
    column_value = ''

    for item in apilist:
        itemlist = item.split("=")
        itemAna = itemlist[0]
        column_name_list = itemlist[1].split('/')
        column_name = '_'.join(column_name_list)
        column = column + column_name + ','
        column_value = column_value + '\'' + itemAna + '\','
    return column, column_value

def insertDBEcg(tablename, column, value):
    '''插入sqlite数据库

    :param column: 列名
    :param value: 值
    :return: bool
    '''
    conn = sqlite3.connect(now_dir+"/log_daily.db")
    cur = conn.cursor()
    try:
        cur.execute("insert into " + tablename + "(" + column + ") values(" + value + ")")
    except Exception, e:
        print e
    conn.commit()
    cur.close()
    conn.close()
    return True

    return sortDictCount

ecgstr, runstr = excute_s()
ecg_column, ecg_value = oprApi(ecgstr)
run_column, run_value = oprApi(runstr)
insertDBEcg('ecg_api', ecg_column.rstrip(','), ecg_value.rstrip(','))
insertDBEcg('run_api', run_column.rstrip(','), run_value.rstrip(','))


class Cecg:
    def GET(self):
        ecgList = showTableStructure('ecg_api')
        return render.cecg(ecgList)


class Crun:
    def GET(self):
        runList = showTableStructure('run_api')
        return render.cecg(runList)


def showTableStructure(tablename):
    '''统计表每个列的总值

    :param tablename: sqlite3 api 的表名
    :return: 返回值是按照值排序后的列表，如 ['user_DoctorInfo=2177=13.94', 'user_UserInfoByID=2038=13.05']
    '''
    countRaw = 0
    now_dir = os.path.split(os.path.realpath(__file__))[0]
    dictCount = {}
    conn = sqlite3.connect(now_dir + "/log_daily.db")
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(" + tablename + ")")
    table_head = cur.fetchall()
    for i in table_head:
        if i[0] == 0 or i[0] == 1:
            continue
        cur.execute("select sum(" + i[1] + ") from " + tablename)
        countColumn = cur.fetchall()
        dictCount[unicode(i[1])] = countColumn[0][0]
        countRaw += countColumn[0][0]
    dictCount['allcount'] = countRaw
    cur.close()
    conn.close()
    sortDictCount = sorted(dictCount.iteritems(), key=lambda d: d[1], reverse=True)
    rlist = []
    for item in sortDictCount:
        if item[0] == 'allcount':
            continue
        f = float(item[1])

        rlist.append(str(item[0]) + "=" + str(item[1]) + "=" + str(round(f * 100 / sortDictCount[0][1], 2)) + " %")
    return rlist
