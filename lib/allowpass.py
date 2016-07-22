#!/usr/bin/python
#coding=utf-8

import conn_redis
import logsys
import md5

class DealWithPwd():

    def __init__(self):
        try:
            self.logs = logsys.LogSys()
        except:
            pass
        try:
            self.credis = conn_redis.CRedis()
        except Exception, e:
            self.logs.writelog(str(e))
        pass

    def allowpwd(self, usr):

        pwd = self.credis.getrange(usr, '0', '-1')
        if pwd == '':
            return(usr, "xhsidunadyadnfbaga1=")
        else:
            return(usr, pwd)
        pass

    def transmd5(self, passwd):

        return md5.md5get(passwd)

# 向redis中添加用户
    def rowin(self, usr, pwd):
        md5pwd = md5.md5get(pwd)
        self.credis.set(usr, md5pwd)
        pass


def test():
    dp = DealWithPwd()
    dp.rowin("admin", "123456")
    dp.rowin("cuibing","cuibin123")
    dp.rowin("guest","123123")
    dp.rowin("show","123123")
    dp.rowin("dev","123123")
    pass

test()