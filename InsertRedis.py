#!/usr/bin/python
#coding=utf-8

from lib.conn_redis import CRedis
from logsys import LogSys
from lib.read_ini import config
import time
from UpWeb import ExcuteConn

STR = "258 ,12 ,0 ,0 ,34 56 23 12 23 11 33 44 21 20 60 60 30 20 10 0 10 ,ios9=41 android6=0 android5=0 android4=22 ," \
      "10=ValidateCode=16.67% 2=UserInfoByID=3.33% 2=UploadImage=3.33% 6=SendPhoneCode=10.00% 8=Register=13.33% " \
      "1=RecordInfo=1.67% 3=OwnLogin=5.00% 1=ModifyUserInfo=1.67% 5=EcGHistoryData=8.33% 6=DeviceLog=10.00% " \
      "16=CheckMobile=26.67%,10=ValidateCode=16.67% 2=UserInfoByID=3.33% 2=UploadImage=3.33% 6=SendPhoneCode=10.00% " \
      "8=Register=13.33% 1=RecordInfo=1.67% 3=OwnLogin=5.00% 1=ModifyUserInfo=1.67% 5=EcGHistoryData=8.33% 6=DeviceLog=10.00% " \
      "16=CheckMobile=26.67%"

def nowtime():
    hour = time.localtime()[3]
    return hour

class insertRedis():
    def __init__(self):
        self.cf = config()
        self.log = LogSys()
        self.cr = CRedis()
        self.shpath = self.cf.getvalue('script_path', 'indexvalue')
        self.ec = ExcuteConn('agency', 1) # 表示需要返回执行的输出str
        pass

    def __getlogvalue(self, tt):
        #return STR
        command = "bash %s" % self.shpath
        # command shpath后不跟参数表示返回整天数据
        try:
            rc = self.ec.allexcute(command)
            if type(rc) == list:
                # 校验返回值类型.
                return str(rc[0])
            else:
                return 9
        except ExcuteConn, e:
            errmsg = "excute allexcute ERR.func __getvalue.%s" % e
            return 9

    def __dealwithstr(self, str):
        list1 = str.split(',')
        if len(list1) == 8 and list1[7] == '\n':
            list1[7] = '0=NoRunUser=100%'
        if len(list1) == 8 and list1[6] == ' ':
            list1[6] = '0=NoEcgUser=100%'
        if len(list1) > 8:
            list1 = list1[:-1]
        else:
            pass
        list2 = ['index_num1', 'index_num2','index_num3', 'index_num4', 'index_line', 'index_o','index_ecg', 'index_run']
        #list2 = ['index_num11', 'index_num21','index_num31', 'index_num41', 'index_line1', 'index_o1','index_ecg1', 'index_run1']
        if len(list1) != len(list2):
            errmsg = "accesslog 截取的字串数量错误.func __getlogvaue."
            print errmsg
            self.log.writelog(errmsg)
            return 9
        else:
            for i in  range(0, len(list2)):
                try:
                    if i < 4:
                        self.cr.set(list2[i], list1[i])
                    else:
                        self.cr.remove(list2[i])
                        #!!!! 这里暂时使用了删除主键的做法,后期需要改为将当天最后时刻的键值读取出来存入数据库然后再删除.
                        for m in list1[i].split(' '):
                            if m != '':
                                self.cr.rrpush(list2[i], m)
                except Exception, e:
                    errmsg = "redis set value error.func __delwithstr. %s" % e
                    self.log.writelog(errmsg)


    def main_C(self, tt = nowtime()):
        rc = self.__getlogvalue(tt)
        if type(rc) == str:
            self.__dealwithstr(rc)
        else:
            return 9


if __name__ == '__main__':
    ir = insertRedis()
    ir.main_C()
