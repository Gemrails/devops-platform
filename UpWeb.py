#!/usr/bin/python
#coding=utf-8

import paramiko
from switch import switch_ip, switch_pwd, switch_username
from lib.read_ini import config
from lib.logsys import LogSys
import threading
import time


class ExcuteConn(object):
    def __init__(self, dev, needstrreturn = 0):
        self.cf = config()
        self.log = LogSys()
        self.ip = switch_ip(dev)
        self.nsr = needstrreturn
        self.port = int(self.cf.getvalue('server_conf', 'port'))
        self.username = switch_username(dev)
        self.password = switch_pwd(dev)
        pass

    # 通用连接执行命令方法,如果需要返回输出,则需要传递needstrreturn 定值为1
    def allexcute(self, command):
        ssh = paramiko.SSHClient()
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip,self.port,self.username,self.password,timeout=5)
            stdin, stdout, stderr = ssh.exec_command(command)
            out = stdout.readlines()
            #屏幕输出
            ssh.close()
            if self.nsr == 0:
                return 5
                # 5是幸运数字,成功的返回值基本都为5
            else:
                return out
        except Exception, e:
            errmsg =  "excuteup Error.allexcute %s" % e
            ssh.close()
            self.log.writelog(errmsg)
            return 0



class UpDate(object):

    def __init__(self, dev, pname):
        self.cf = config()
        self.log = LogSys()
        self.pname = pname
        self.ip = switch_ip(dev)
        self.port = int(self.cf.getvalue('server_conf', 'port'))
        self.localpath = self.cf.getvalue('write_path', 'upfilepath') + self.pname + ".zip"
        self.remotepath = self.cf.getvalue('write_path', 'topath') + self.pname + ".zip"
        self.username = switch_username(dev)
        self.password = switch_pwd(dev)

    def __trans_file(self):
        try:
            tus = (self.ip, self.port)
            t = paramiko.Transport(tus)
            t.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(t)
            sftp.put(self.localpath, self.remotepath)
            t.close()
            print "trans_ok"
            return 5
        except Exception, e:
            print "put_file:" + str(e)
            return 0

    def __excuteup(self):
        #执行部分
        ssh = paramiko.SSHClient()
        comm = '/root/resvn.sh ' + self.pname
        #print comm
        try:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.ip,self.port,self.username,self.password,timeout=10)
            stdin, stdout, stderr = ssh.exec_command(comm)
            out = stdout.readlines()
            #屏幕输出
            ssh.close()
            #print out
            return 5
        except Exception, e:
            errmsg =  "excuteup Error.__excute" + str(e)
            ssh.close()
            self.log.writelog(errmsg)
            return 0

    def runup(self):
        if self.__trans_file():
            if self.__excuteup():
                print "update success."
                return 5
            else:
                print "trans OK. excute ERR!"
                return 1
        else:
            return 1

def main_c(dev, pname):

    up = UpDate(dev, pname)
    rc = up.runup()
    return rc

def thread_up(pname):
    # 把线程池单独拿出来写到一个lib中集中调用.
    cf = config()
    log = LogSys()
    ll = cf.getvalue('devname', 'web_dev')
    ldev = ll.split(',')
    threadpool = []
    try:
        for dev in ldev:
            tp = threading.Thread(target=main_c, args=(dev, pname))
            threadpool.append(tp)

        for th in threadpool:
            time.sleep(0.1)
            th.start()

        for th in threadpool:
            th.join()
            print "main exit."

        return 5
    except Exception, e:
        errmsg = "threadError.func thread_up." + str(e)
        log.writelog(errmsg)
