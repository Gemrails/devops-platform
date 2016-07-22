#!/usr/bin/env python
# coding=utf-8

import sqlite3
import sys

class oprSqlitDB:
	def __init__(self,dbname):
		self._conn = sqlite3.connect(dbname)
		self._conn.text_factory=lambda x: unicode(x, "utf-8", "ignore")
		self._cur = self._conn.cursor()
	def dbExecute(self,sql):
		self._cur.execute(sql)
		res = self._cur.fetchall()
		return res
	def dbClose(self):
		self._cur.close()
		self._conn.close()
