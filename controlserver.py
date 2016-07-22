#!/usr/bin/python
#-*- coding: utf-8 -*-

import paramiko
#from paramiko import AutoAddPolicy, SSHClient, Transport, SFTPClient 
import threading
import time
import sys
import os
#from goto import goto, label


PORT = 22
username = "root"  #用户名
passwd = "mHealth123"    #密码
iplist_web = ['10.172.190.8','10.51.69.209','10.44.173.103']
#iplist_web = ['10.18.121.37']
iplist_sql = ['10.44.164.78','10.51.69.131','10.51.68.120']


def switch_ip(args):

    #使用字典来模拟了一个switch，如果键不存在则返回默认值None
    try:
        result={
        'reg':'10.1.1.1',
        'biz':'10.1.1.1',
        'web_m':'10.1.1.1',
        'web_b':'10.1.1.1',
        'web_s':'10.1.1.1',
        'redis':'10.1.1.1',
        'test':'10.18.121.27',
        'agency':'123.57.86.5'
        }
        if '.' in args:
            ssh2(args)
        else:
            ssh2(result.get(args))
    except Exception, e:
        print str(e)


def getcmd():

    strCmd = raw_input("command input: ")
    #做一些类似校验的处理。暂时没有
    #print strCmd
    return strCmd


def ssh2(ip):

    try:
        #print ip
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        username = raw_input("username:")
        if ip == '123.57.86.5':
            passwd = 'bjmHealth365'
        else:
            passwd = raw_input("password:")
        try:
            ssh.connect(ip,22,username,passwd,timeout=10)
        except Exception, e:
            print "Can't connect!"
            print str(e)

        while(1):

            cmd = getcmd()
            if cmd == "exit":
                break
            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdin.write("Y")   #简单交互，输入 ‘Y’ 
            out = stdout.readlines()

            #屏幕输出
            for o in out:
                print o,

            continue
        print "\n\tssh connection is order to be closed.\n"
        ssh.close()
    except Exception, e :
        print str(e)
        print '%s\tError\n'%(ip)


def send_webfile(ip):

    #上传web文件
    t = paramiko.Transport((ip,PORT)) 
    t.connect(username = username, password = passwd) 
    sftp = paramiko.SFTPClient.from_transport(t) 
    remotepath='/root/svn_online.zip' 
    localpath='/root/svn_online.zip' 
    sftp.put(localpath,remotepath) 
    t.close() 

    #print "sendfile\n"


def send_sqlfile(ip,sqlname):

    #上传sql文件 
    #print "timeout!"
    #return
    t = paramiko.Transport((ip,PORT)) 
    t.connect(username = username, password = passwd) 
    sftp = paramiko.SFTPClient.from_transport(t) 
    remotepath='/root/mhealth_' + sqlname + '.sql'
    localpath='/root/mhealth_' + sqlname + '.sql'
    sftp.put(localpath,remotepath) 
    t.close() 

    #print "sendfile"

def excute_sql(ip):

    #执行部分
    ssh = paramiko.SSHClient()
    comm = '/root/upsql.sh'
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,PORT,username,passwd,timeout=10)
    stdin, stdout, stderr = ssh.exec_command(comm)
    out = stdout.readlines()
    #屏幕输出
    for o in out:
        print o
    ssh.close()


def excuteup(ip):

    #执行部分
    ssh = paramiko.SSHClient()
    comm = '/root/upsvn.sh'
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,PORT,username,passwd,timeout=10)
    stdin, stdout, stderr = ssh.exec_command(comm)
    out = stdout.readlines()
    #屏幕输出
    for o in out:
        print o
    ssh.close()

    #print "\nexcute update\n"


def printerr():

    #提示
    print "\n\tuse 'maincont.py upweb' to sftp your file to the webserver."
    print "\tuse 'maincont.py upsql' to sftp your file to the webserver."
    print "\tuse 'maincont.py et' to excute server's shell update webproject."
    print "\tuse 'maincont.py id(reg/biz/sreg/sbiz)' to start sqlconn service.\n"


def conn_sql(arg):

    if 'id' == arg:
        os.system('cp /phpstudy/www/phpmyadmin/.config.inc.php_id /phpstudy/www/phpmyadmin/config.inc.php')
    elif 'reg' == arg:
        os.system('cp /phpstudy/www/phpmyadmin/.config.inc.php_reg /phpstudy/www/phpmyadmin/config.inc.php')
    elif 'sreg' == arg:
        os.system('cp /phpstudy/www/phpmyadmin/.config.inc.php_sreg /phpstudy/www/phpmyadmin/config.inc.php')
    elif 'biz' == arg:
        os.system('cp /phpstudy/www/phpmyadmin/.config.inc.php_biz /phpstudy/www/phpmyadmin/config.inc.php')
    elif 'sbiz' == arg:
        os.system('cp /phpstudy/www/phpmyadmin/.config.inc.php_sbiz /phpstudy/www/phpmyadmin/config.inc.php')

    elif 'stop' == arg:
        try:
            os.remove('/phpstudy/www/phpmyadmin/config.inc.php')
        except Exception, e:
            #print str(e)
            print "\n\tThere was no config.\n"
        os.system('/phpstudy/server/httpd/bin/apachectl stop')
        print "\n\tService has been closed.\n"
        sys.exit(0)
    else:
        sys.exit(1)
    os.system('/phpstudy/server/httpd/bin/apachectl start')
    print "\n\tService has been open.\n"


def send_w():

    for ip in iplist_web:
        send_webfile(ip)
        time.sleep(0.5)
        excuteup(ip)

def control_main(arg):
    os.system('clear')
    print "\nBegin...\n" 
    if 'upweb' == arg:
        send_w()
    elif 'upsql' == arg:
        send_s()
    elif 'et' == arg:
        excuteup()
    elif 'hh' == arg:
        printerr()
    else:
        conn_sql(arg)


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
        switch_ip(sys.argv[2])
