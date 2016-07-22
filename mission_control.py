#!/usr/bin/python
#-*- coding: utf-8 -*-

import paramiko
import sys
import os
from switch import switch_ip, devname, switch_pwd

PORT = 22


def getcmd():

    strCmd = raw_input("command input: ")
    # 做一些类似校验的处理。暂时没有
    # print strCmd
    return strCmd


def ssh2(args):

    try:
        ip = switch_ip(args)
        #print ip
        dev_name = devname(ip)
        print "\nConnecting to " + dev_name
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        username = raw_input("username:")
        passwd = switch_pwd(dev_name) 

        try:
            ssh.connect(ip,22,username,passwd,timeout=10)
        except Exception, e:
            print "Can't connect!\n" + str(e)

        while(1):

            cmd = getcmd()
            if cmd == "exit":
                os.system('clear')
                break
            if 'sscp' in cmd:
                filelist = cmd.split('/')[1:]
                #print filelist
                for fl in filelist:
                    #print fl
                    up_file(ip, fl, username, passwd)

            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdin.write("Y")   #简单交互，输入 ‘Y’ 
            out = stdout.readlines()

            #屏幕输出
            for o in out:
                print o,

            continue
        print "\n\tssh connection is order to be closed.\n"
        ssh.close()
    except Exception, e:
        print str(e)
        print '%s\tError\n'%(ip)


def up_file(ip, filename, username, password):

    try:
        print "timeout"
        # return
        t = paramiko.Transport((ip,PORT)) 
        t.connect(username = username, password = password) 
        sftp = paramiko.SFTPClient.from_transport(t) 
        print "Put ur file into ./upload/ !"
        remotepath = '/root/' + filename
        localpath = './upload/' + filename
        sftp.put(localpath,remotepath) 
        t.close() 

        print "sendfile"
    except Exception, e:
        print "put_file:" + str(e)
    

#threads = []   #多线程
#    ssh2(ip,username,passwd,cmd)
'''
    for i in range(1,254):
        ip = '192.168.1.'+str(i)
        a=threading.Thread(target=ssh2,args=(ip,username,passwd,cmd)) 
        a.start()
'''

if __name__ == '__main__':

    if len(sys.argv) == 3 and sys.argv[1] == 'ssh':
        ssh2(sys.argv[2])
