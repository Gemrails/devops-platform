#!/usr/bin/python
#coding=utf-8

import commands
import struct
import time
import read_ini

# 配置文件路径在代码中写成了不输入则使用默认,在布置时需要记得修改这个路径.
#INIFILE = '/Users/pujielan/Documents/code/web_upload/auto_config.ini'

LOGHOME = '/var/log/'

ExcuError = "request failed!"

class TransTime(object):

    __format_time = "4s2s2s"

    def __init__(self):
        pass

    def __month(self, mon):
        result={
        '01':'Jan',
        '02':'Feb',
        '03':'Mar',
        '04':'Apr',
        '05':'May',
        '06':'Jun',
        '07':'Jul',
        '08':'Aug',
        '09':'Sep',
        '10':'Oct',
        '11':'Nov',
        '12':'Dec'
        }
        return result.get(mon)

    def __localtime():
        # 此处属于内部函数,不加self
        TIMEFORMAT = '%Y%m%d'                # Y 2016年  y 16年
        nowtime = time.strftime(TIMEFORMAT, time.localtime())
        #print nowtime
        return nowtime

    def http_time(self, ymd = __localtime()):
        #print ymd  # 默认显示当天当时刻日志  时间格式为 20160108
        time1 = struct.unpack(self.__format_time, ymd)
        showt = time1[2]+'/'+self.__month(time1[1])+'/'+ time1[0]
        #print showt
        return showt

    def php_time(self, ymd = __localtime()):

        time1 = struct.unpack(self.__format_time, ymd)
        showt = time1[0]+'/'+time1[1]+'/'+time1[2]
        return showt
        #print "php_time" + ymd
        pass

    def nginx_time(self, ymd = __localtime()):

        #print "nginx_time" + ymd
        # [13/Jan/2016:16:36:03 +0800]
        time1 = struct.unpack(self.__format_time, ymd)
        showt = time1[2]+'/'+self.__month(time1[1])+'/'+time1[0]
        print showt
        return showt
        pass

    def error_http_time(self, ymd = __localtime()):

        # print "error.log time"
        time2 = struct.unpack(self.__format_time, ymd)
        # [Thu Jul 23 10:20:46.051417 2015]
        showt = self.__month(time2[1]) + " " + time2[2]
        #print showt
        return showt

    def status_time(self, ymd = __localtime()):

        #print "status_time" + ymd
        pass

    def agency_wtmptime(self, ymd = __localtime()):

        time2 = struct.unpack(self.__format_time, ymd)
        # 2016-01-18
        showt = time2[0] + "-" + time2[1] + "-" + time2[2]
        print showt

class ExcuteHttperror(object):

    # eg:[Fri Jan 08 10:41:24.989711 2016]
    def __init__(self, ttime):
        self.ttime = ttime

    pass

    def test_module(self):
        '''
            test module仅用于调试当天的日志
        '''
        listlog = []
        logFile = open(self.filepath, 'r')
        logFile.seek(0, 2)
        logFile.seek(-4500, 2)
        rowcount = 0
        for row in logFile.readlines()[1:]:
            listlog.append(row)
            #print row
            rowcount += 1
        return listlog

        #logFile.seek()

class AgencySafe(object):
    '''
        用于监控wtmp和secure中的系统登录日志
    '''

    def __init__(self, ttime):
        self.ttime = ttime
        pass

    def login_wtmp(self):

        command1 = "who /var/log/wtmp | grep %s " %(self.ttime)
        (status, output) = commands.getstatusoutput(command1)
        if 0 == status:
            print "\n-- %s 当天登录的IP如下: --" %(self.ttime)
            print str(output) + '\n'
            return output
        else:
            print "request failed!"
            return 9

    def login_secure(self, lnum):

        command1 = "tail -n %d /var/log/secure "%(lnum)
        (status, output) = commands.getstatusoutput(command1)
        if 0 == status:
            print "\n-- 登录记录为: -- "
            print str(output)
            return output
        else:
            print "request failed!"
            return 9

class ExcutePhperror(object):
    '''
        web_php_db_error
        ecg_application_error
        web_application_error
        run_application_error
        doc...
        cr...
    '''

    def __init__(self, ttime, logpath):
        self.ttime = ttime
        self.logpath = logpath

    def err_nums(self, lnum):

        command1 = "cat %s | grep %s | grep [error] | cut -c 29- | sort | uniq -c | sort -nr | head -n %d" %(self.logpath, self.ttime, lnum)
        filename = self.logpath.split("/")[-1]
        print filename
        (status, output) = commands.getstatusoutput(command1)
        if 0 == status and output != '':
            print "\n-- %s 当天%s报错前%d为 -- " % (self.ttime, filename, lnum)
            print str(output) + '\n'
            return output
        elif 0 == status and output == '':
            print "\n-- %s 当天%s没有报错信息 -- "  % (self.ttime, filename)
        else:
            print "request failed!"
            return 9

    def tail_status(self, lnum):

        command1 = "tail -n %d %s | grep %s | cut -c 29- " % (lnum, self.logpath, self.ttime)
        filename = self.logpath.split("/")[-1]
        print filename
        (status, output) = commands.getstatusoutput(command1)
        if 0 == status and output != '':
            print "\n-- %s当天%s实时日志 -- " %(self.ttime, self.logpath)
            print str(output) + '\n'
        elif 0 == status and output == '':
            print "\n-- %s当天实时日志暂无 -- " %(self.ttime)
        else:
            print "request failed!"
            return 9

    def test_module(self):
        '''
            test module仅用于调试当天的日志
        '''
        listlog = []
        logFile = open(self.filepath, 'r')
        logFile.seek(0, 2)
        logFile.seek(-4500, 2)
        rowcount = 0
        for row in logFile.readlines()[1:]:
            listlog.append(row)
            #print row
            rowcount += 1
        return listlog

        #logFile.seek()

class ExcuteHttpstatus(object):
    '''
        apache log --- access_log
    '''
    def __init__(self, ttime, logpath):
        self.ttime = ttime
        self.logpath = logpath

    def ipnums(self):

        command1 = "cat %s | grep %s | awk '{print $2}' | sort | uniq -c | sort -nr" %(self.logpath, self.ttime)
        #print command1
        (status, output) = commands.getstatusoutput(command1)
        if 0 == status and output != '':
            print "\n-- %s 当天的ip连接数为 %s -- " %(self.ttime, output[:-2])
            return output[:-2]
        elif 0 ==status and output == '':
            print "\n-- %s 当天没有记录. -- " %(self.ttime)
            return 0
        else :
            print "request failed!"
            return 9
        pass

    def url_nums(self, lnum):

        # 读取配置文件中的ip
        ipstr = '10.18.1.150'
        command2 = "cat %s | grep %s | grep %s | awk '{print $7}' | sort | uniq -c | sort -nr | head -n %d" %(self.logpath, self.ttime, ipstr, lnum)
        #print command2
        (status, output) = commands.getstatusoutput(command2)
        #print type(output)
        if 0 == status and output != '':
            print "\n-- %s 当天前%d的url访问如下: -- " %(self.ttime, lnum)
            print str(output) + '\n'
            pass
            return output
        elif 0 == status and output == '':
            print "\n-- %s 当天没有记录. -- " %(self.ttime)
            return 0
        else:
            print "request failed!"
            return 9

    def increase_500(self, lnum):

        ipstr  = '10.18.1.150'
        command3 = "cat %s | grep %s | grep %s | awk '{print $9}' | sort | uniq -c | sort -nr | head -n %d" %(self.logpath, self.ttime, ipstr, lnum)
        #print command3
        (status, output) = commands.getstatusoutput(command3)
        if 0 == status and output != '':
            print "\n-- %s 当日状态码如下: -- "% (self.ttime)
            print str(output) + '\n'
            pass
            return output
        elif 0 == status and output == '':
            print "\n-- %s 当天没有记录. -- " %(self.ttime)
            return 0
        else:
            print "request failed!"
            return 9
        pass

    def hot_time(self,lnum):

        command4 = "cat %s | grep %s | awk '{print $4}' |cut -c 14-18|sort|uniq -c|sort -nr|head -n %d" %(self.logpath, self.ttime, lnum)
        (status, output) = commands.getstatusoutput(command4)
        if 0 == status and output != '':
            print "\n-- %s 当日热点时间为: -- "% (self.ttime)
            print str(output) + '\n'
            pass
            return output
        elif 0 == status and output == '':
            print "\n-- %s 当天没有记录. -- " %(self.ttime)
            return 0
        else:
            print "request failed!"
            return 9
        pass

    def test_module(self):
        '''
            test module仅用于调试当天的日志
        '''
        listlog = []
        logFile = open(self.filepath, 'r')
        logFile.seek(0, 2)
        logFile.seek(-4500, 2)
        rowcount = 0
        for row in logFile.readlines()[1:]:
            listlog.append(row)
            #print row
            rowcount += 1
        return listlog

        #logFile.seek()

class NginxStatus(object):

    '''
    nginx access_log
    '''
    def __init__(self, ttime, filepath):

        import writefile
        self.wp = writefile.WritePath(INIFILE)
        self.ttime = ttime
        self.filepath = filepath
        print self.ttime
        print self.filepath
        pass

    def ipnums(self):

        command1 = "cat  %s | grep %s | awk '{print $1}' | sort | uniq -c | wc -l " %(self.filepath, self.ttime)
        (status, output) = commands.getstatusoutput(command1)
        if 0 == status and output != '':
            strt ="\n\n%s 当天的ip连接数为%s --" %(self.ttime, int(output))
            self.wp.write_file(strt)
            return int(output)
        else:
            print ExcuError
            return 9

    def hot_urls(self, nums):

        command1 = "cat %s | grep %s | awk '{print $7$11}' | sort | uniq -c | sort -nr | head -n %d" %(self.filepath, self.ttime, nums)
        (status, output) = commands.getstatusoutput(command1)
        if 0 == status and output != '':
            strt = "\n\n%s 当天前%d的url访问为: -- \n" %(self.ttime, nums)
            self.wp.write_file(strt)
            self.wp.write_file(output)
            #print output
            return output
        elif 0 == status and output == '':
            strt =  "\n\n%s 当天没有url访问记录. -- " %(self.ttime)
            self.wp.write_file(strt)
            return 0
        else:
            print ExcuError
            return 9

    def increase_500(self, nums):

        command1 = "cat %s | grep %s  | awk '{print $9}' | sort | uniq -c | sort -nr | head -n %d" %(self.filepath, self.ttime, nums)
        (status, output) = commands.getstatusoutput(command1)
        if 0 == status and output != '':
            strt = "\n\n%s 当天访问的状态码为: -- \n"%(self.ttime)
            self.wp.write_file(strt)
            self.wp.write_file(output)
            print output
            return output
        elif 0 == status and output == '':
            strt = "\n\n%s 当天没有状态码记录. -- "%(self.ttime)
            self.wp.write_file(strt)
            return 0
        else:
            print ExcuError
            return 9

    def hot_time(self, nums):

        command1 = "cat %s | grep %s | grep '/api/iphone' | awk '{print $4}' |cut -c 14-18|sort|uniq -c|sort -nr|head -n %d" %(self.filepath, self.ttime, nums)
        (status, output) = commands.getstatusoutput(command1)
        if 0 == status and output != '':
            strt = "\n\n%s 当天热点时间为: -- \n"%(self.ttime)
            self.wp.write_file(strt)
            self.wp.write_file(output)
            #print output
            return output
        elif 0 == status and output == '':
            strt = "\n\n%s 当天没有访问热点记录. -- " %(self.ttime)
            self.wp.write_file(strt)
            return 0
        else:
            print ExcuError
            return 9

    def test_module(self):
        '''
            test module仅用于调试当天的日志
        '''
        listlog = []
        logFile = open(self.filepath, 'r')
        logFile.seek(0, 2)
        logFile.seek(-4500, 2)
        rowcount = 0
        for row in logFile.readlines()[1:]:
            listlog.append(row)
            #print row
            rowcount += 1
        return listlog

        #logFile.seek()

    def get_urlstatus(self, url = 'http://127.0.0.1:9900/nginx_status'):
        '''
            获取 nginx status状态
        '''
        import urllib2
        response = urllib2.urlopen(url)
        html = response.read()
        status_num = html.split('\n')[2]
        print status_num
        strt = "\n\n%s nginx创建的握手连接数为: -- \n" %(self.ttime)
        #print strt
        self.wp.write_file(strt)
        self.wp.write_file(status_num)
        return status_num

        pass

class mysqlError(object):

    def __init__(self):
        pass

class DailyShow(object):
    def __init__(self):
        pass




if __name__ == '__main__':

    readcf = read_ini.config()
    '''获取日志文件路径'''
    try:
        everypath = readcf.getvalue('logpath_conf', 'http_status')
        print everypath
    except Exception, e:
        print "getpath Error!" + str(e)

    #httptime1 = TransTime()
    #httptime1.agency_wtmptime()
    nginxtime1 = TransTime()
    nginxtime1.nginx_time("20160311")

    #nginxstatus = NginxStatus(nginxtime1.nginx_time("20160312"), readcf.getvalue('logpath_conf', 'nginx_status'))
    #nginxstatus.ipnums()
    #nginxstatus.hot_urls(20)
    #nginxstatus.hot_time(20)
    #nginxstatus.get_urlstatus('http://ecg.mhealth365.cn:9900/nginx_status')
    #try:
    #    httptime1 = TransTime()
    #    #httptime1.http_time("20190902")
    #    httptime1.error_http_time()
    #    phptime = httptime1.php_time()
    #except Exception, e:
    #    print "gettime Error!" + str(e)

    #excute_php_error1 = ExcutePhperror(phptime, readcf.getvalue('logpath_conf', 'php_dberror_log'))
    #excute_php_error1.err_nums(6)

    #excute_http_status1 = ExcuteHttpstatus(httptime1.http_time("20160104"))
    #excute_http_status1.ipnums()
    #excute_http_status1.url_nums()
    #excute_http_status1.increase_500()
    #excute_http_status1.hotclick_time()

    #read_ini.write_in("/Users/pujielan/Documents/code/web_upload/auto_config.ini", "safe_status", "login_log", "/var/log/wtmp")
