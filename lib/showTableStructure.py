#!/usr/bin/env python
# coding=utf-8

import sqlite3
import os, sys

from oprSqlite3DB import oprSqlitDB

class apiTable:
	def __init__(self,tablename,db_dir):
		self._tablename = tablename
		self._dbdir = db_dir
		#print self._tablename, self._dbdir

	def oprDB(self):
		'''统计表每个列的总值

		:param tablename: sqlite3 api 的表名
		:return: 返回值是按照值排序后的列表，如 ['user_DoctorInfo=2177=13.94', 'user_UserInfoByID=2038=13.05']
		'''
		countRaw = 0
		dictCount = {}
		
		sqlitedb = oprSqlitDB(self._dbdir)
		table_head = sqlitedb.dbExecute("PRAGMA table_info("+self._tablename+")")

		for i in table_head:
			if i[0] == 0 or i[0] == 1:
				continue
			countColumn = sqlitedb.dbExecute("select sum(" + i[1] + ") from " + self._tablename)
			dictCount[unicode(i[1])] = countColumn[0][0]
			countRaw += countColumn[0][0]
		dictCount['allcount'] = countRaw
		
		sqlitedb.dbClose()

		sortDictCount = sorted(dictCount.iteritems(),key=lambda d:d[1], reverse=True)
		rlist = []
		for item in sortDictCount:
			if item[0]=='allcount':
				continue
			f = float(item[1])
			
			rlist.append(str(item[0])+"="+str(item[1])+"="+str(round(f*100/sortDictCount[0][1],2))+" %")
		return rlist
