#!/usr/bin/python
#coding=utf-8

import json
import urllib2
import ssl
from conn_redis import CRedis

class GetToken(object):
    def __init__(self, user, passwd, eauthway, host="127.0.0.1", port="8000"):
        '''
        在测试时默认使用本机127ip 和 8000的端口  在实际使用时,需要传递正确的ip和端口
        :param user:
        :param passwd:
        :param eauthway:
        :param host:
        :param port:
        :return:
        '''
        self.credis = CRedis()
        self.user = user
        self.passwd = passwd
        self.eauth = eauthway
        self.url = "https://%s:%s/" % (host, port)
        self.header = {"Content-Type":"application/json", "Accept":"application/json"}

    def __request(self, url, pdata=None, header=None):
        return urllib2.Request(url, pdata, header)
        pass

    def __response(self, url, pdata=None, header=None):
        __jpostdata = json.dumps(pdata)
        __request = urllib2.Request(url, __jpostdata, header)
        __response = urllib2.urlopen(__request)
        return __response
        pass

    def gettoken(self):
        '''
        https://127.0.0.1:8000/login/
        :return:
        '''
        self.token_key = "%s-token" % self.user
        if self.credis.iexist(self.token_key):
            token = self.credis.get(self.token_key)
            return token
        else:
            __post_data = [{"username":self.user, "password":self.passwd, "eauth":self.eauth}]
            __turl = self.url + "login/"
            print __turl
            response = self.__response(__turl, __post_data, self.header)
            html = json.loads(response.read())
            token = html.get("return")[0].get("token")
            try:
                self.credis.set(self.token_key, token)
                self.credis.eexpire(self.token_key)
            except Exception, e:
                print "gottoken errmsg: %s " % e
            # 将生成的token 插入到redis
            return token
        pass

    def excute(self, _token, client, tgt, fun):
        '''
        https://127.0.0.1:8000/
        :param _token:
        :param client:
        :param tgt:
        :param fun:
        :return:
        '''
        __pre_data = [{"client":client, "tgt":tgt, "fun":fun}]
        header = {"Content-Type":"application/json", "Accept":"application/x-yaml", "X-Auth-Token":_token}
        response = self.__response(self.url, __pre_data, header)
        html = response.read()
        print html
        pass

    def minion_status(self, _token):
        '''
        https://127.0.0.1:8000/minions
        :param _token:
        :return:
        '''
        murl = self.url + "minions/"
        header = {"Accept":"application/x-yaml", "X-Auth-Token":_token}
        response = self.__response(murl, '', header)
        html = response.read()
        print html

    def job_list(self, _token):
        '''
        https://127.0.0.1:8000/jobs/
        :param _token:
        :return:
        '''
        jurl = self.url + 'jobs/'
        header = {"Accept":"application/x-yaml", "X-Auth-Token":_token}
        response = self.__response(jurl, '', header)
        html = response.read()
        urllib2.urlopen()
        print html
        pass

    def __excuteMode(self, _token, client, fun):
        '''
        https://127.0.0.1:8000/
        :param _token:
        :return:
        '''
        __p_data = [{"client":client, "fun":fun}]
        header = {"Accept":"application/json", "X-Auth-Token":_token}
        response = self.__response(self.url, __p_data, header)
        html = json.loads(response.read())
        response.close()
        print html

    def _wheel(self, _token):
        '''
        https://127.0.0.1:8000/
        :param _token:
        :return:
        '''

        pass

    def _runsls(self, _token, client, tgt, slsfile, testsign=False):

        testarg = "test=%s" % testsign
        __rpdata = [{"client":client, "tgt":tgt, "fun":"state.sls", "arg":slsfile}]
        header = {"Content-Type":"application/json", "Accept":"application/json", "X-Auth-Token":_token}
        response = self.__response(self.url, __rpdata, header)
        html = json.loads(response.read())
        response.close()
        print html

        pass


def test():
    pre_data = [{"client":"local", "tgt":"*", "fun":"test.ping"}]
    json_data = json.dumps(pre_data)

    header = {"Content-Type":"application/json", "Accept":"application/json", "X-Auth-Token":"697adbdc8fe971d09ae4c2a3add7248859c87079"}

    request = urllib2.Request(token_url, json_data, header)
    response = urllib2.urlopen(request)

    html = response.read()
    print html

def gettoken():
    post_data = [{"username":"salt", "password":"123123", "eauth":"pam"}]
    json_post_data = json.dumps(post_data)

    header = {"Content-Type":"application/json", "Accept":"application/json"}
    request = urllib2.Request(token_url, json_post_data, header)
    response = urllib2.urlopen(request)

    html = json.loads(response.read())
    # 已json格式化获取的返回
    # {u'return': [{u'perms': [u'.*'], u'start': 1469435268.361253, u'token': u'0da0faf38d020a6433d0443389ebe6481c7d68f6', u'expire': 1469478468.361253, u'user': u'salt', u'eauth': u'pam'}]}
    # 实验当中,使用了salt的方式,获得html返回为json的dict模式,使用字典取值方式获得token
    print html.get("return")[0].get("token")



    print html


if __name__=="__main__":
    gett = GetToken('salt', '123123', 'pam')
    gett.excute()
