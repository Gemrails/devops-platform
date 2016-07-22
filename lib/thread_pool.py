#!/usr/bin/python
#coding=utf-8

import threading
import time

class ThreadPool(object):
    def __init__(self):
        self.threadpool = []
        pass

    def creatappend(self, ptarget, argus):
        tp = threading.Thread(target=ptarget, args=argus)
        self.threadpool.append(tp)

    def thgo(self):
        for th in self.threadpool:
            time.sleep(0.01)
            th.start()

        for th in self.threadpool:
            th.join()

def main_c(num):
    for i in range(1,num):
        print "num %d, %d" %(num, i)
        time.sleep(1)
    return 1

def test():

    tl = ThreadPool()
    for num in ([10], [20], [30]):
        print type(num)
        tl.creatappend(main_c, num)

    tl.thgo()

if __name__ == '__main__':
    test()
    #main_c(5)

