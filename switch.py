#!/usr/bin/python
#-*- coding: utf-8 -*-

from base64 import decodestring as dcs


def switch_ip(args):

    # 使用字典来模拟了一个switch，如果键不存在则返回默认值None
    try:
        result={
        'reg_m':'10.51.69.131',
        'biz_m':'10.51.68.120',
        'web_m':'10.172.190.8',
        'web_b':'10.51.69.209',
        'web_s':'10.44.173.103',
        'redis':'10.44.164.78',
        'reg_s':'10.51.56.153',
        'biz_s':'10.44.168.134',
        'test':'192.168.37.132',
        'test114':'192.168.38.114',
        'agency':'123.57.86.5',
        'support':''
        }
        if '.' in args:
            return args
        else:
            return result.get(args)
    except Exception, e:
        print "switch_ip" + str(e)

# 使用一正一反两个字典，提高效率

def devname(args):

    try:
        dev={
        '123.57.86.5':'agency',
        '10.172.190.8':'web_m',
        '10.51.69.209':'web_b',
        '10.44.173.103':'web_s',
        '10.44.164.78':'redis',
        '10.51.69.131':'reg_m',
        '10.51.56.153':'reg_s',
        '10.51.68.120':'biz_m',
        '10.44.168.134':'biz_s',
        '192.168.38.114':'test'
        }
        return dev.get(args)
    except Exception, e:
        print "devname" + str(e)


def switch_pwd(args):

    # 密码表
    try:
        pwd={
        'reg_m':'bUhlYWx0aDEyMw==',
        'biz_m':'bUhlYWx0aDEyMw==',
        'web_m':'bUhlYWx0aDEyMw==',
        'web_b':'bUhlYWx0aDEyMw==',
        'web_s':'bUhlYWx0aDEyMw==',
        'redis':'bUhlYWx0aDEyMw==',
        'reg_s':'bUhlYWx0aDEyMw==',
        'biz_s':'bUhlYWx0aDEyMw==',
        'agency':'YmptSGVhbHRoMzY1',
        'test114':'MTIzNDU2'
        }
        return dcs(pwd.get(args))
    except Exception, e:
        print "switch_pwd" + str(e)

def switch_username(args):

    # 用户表
    try:
        pwd={
        'reg_m':'cm9vdA==',
        'biz_m':'cm9vdA==',
        'web_m':'cm9vdA==',
        'web_b':'cm9vdA==',
        'web_s':'cm9vdA==',
        'redis':'cm9vdA==',
        'reg_s':'cm9vdA==',
        'biz_s':'cm9vdA==',
        'test114':'cm9vdA==',
        'agency':'cm9vdA=='
        }
        return dcs(pwd.get(args))
    except Exception, e:
        print "switch_username" + str(e)
