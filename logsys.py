#!/usr/bin/python
#coding = utf-8

'''
log system
format:

02/29/2016 14:23:34 function name - Exception e-    \n

'''

import logging
import logging.config

CPATH = 'logconfig.ini'

class LogSys():

    def __init__(self):

        self.logging = logging
        self.path = CPATH

    def writelog(self, excep):

        try:
            self.logging.config.fileConfig(self.path)
            self.logging.info(str(excep))
            self.logging.debug(str(excep))
            self.logging.warning(str(excep))
            self.logging.error(str(excep))
            self.logging.exception(str(excep))
        except Exception, e:
            print str(e)
        #logging.basicConfig(filename = 'log.txt', filemode = 'a', level = logging.ERROR, format = '%(asctime)s - %(levelname)s: %(message)s')
        #logging.disable(30)#logging.WARNING
        #logging.addLevelName(88,"MyCustomError")
        #logging.log(88,"this is an my custom error")


def TestLogBasic():

    logs = LogSys()
    try:
        raise Exception('this is a exception')
    except Exception, e:
        print "1231" + str(e)
        logs.writelog(str(e))
   # logging.shutdown()

#TestLogBasic()
