#coding:utf-8

import hashlib

def md5get(stri):
    m = hashlib.md5()
    m.update(stri)
    pwd = m.hexdigest()
    #print "\nyour passwd is:\n" + stri
    #print "MD5 is:\n" + pwd + '\n'
    return pwd


def checknum(stri):
    if stri+'X' == 'X':
        getnum()
    else:
        md5get(stri)


def getnum():
    stri = raw_input("input your password:")
    checknum(stri)

if __name__=='__main__':
    getnum()
