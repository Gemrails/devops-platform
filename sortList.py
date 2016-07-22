#!/usr/bin/python
#coding=utf-8

from lib.conn_redis import CRedis

# redis中设置两个键,1. 序列 2.最小数值
class SorList(object):
    def __init__(self):
        self.cr = CRedis()
        pass


# 处理方法不太适合大并发,日后需要修改此处.
    def sortnum(self, proj, value):
        self.key = proj
        self.value = value
        if not self.cr.iexist(self.key):
            self.cr.rrpush(self.key, self.value)
            return
        listg = self.cr.llrange(self.key, 0, -1)
        if len(listg)!= 1 and len(listg) < 10:
            for mm in range(0, len(listg)):
                if int(self.value.split('=')[1]) > int(listg[mm].split('=')[1]):
                    listg.insert(mm, self.value)
                    break
            self.cr.rrpush(self.key, self.value)
            return
        elif len(listg) == 1:
            if int(self.value.split('=')[1]) > int(listg[0].split('=')[1]):
                listg.insert('1', self.value)
            else:
                self.cr.rrpush(self.key, self.value)
                return

        else:
            for mm in range(0,10):
                if int(self.value.split('=')[1]) > int(listg[mm].split('=')[1]):
                    listg.insert(mm, self.value)
                    listg = listg[:9]
                    break
        if self.cr.remove(self.key):
            for mm in listg:
                self.cr.rrpush(self.key, mm)

    def getlist(self, proj):
        listg = self.cr.llrange(proj, 0, -1)
        gstr = (';').join(listg)
        print gstr


if __name__ == '__main__':
    sl = SorList()
    sl.getlist('2048')









