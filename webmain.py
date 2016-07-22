#!/usr/bin/env python
# coding: utf-8
import web
from web import form
import os
import ConnPass
import InitStr
from lib.write_file import WriteFile
from lib.allowpass import DealWithPwd
from GetErrlog import ExcuteErrLog
import time
from logsys import LogSys
import UpWeb as up
from lib.showTableStructure import apiTable
from lib.read_ini import config

log = LogSys()
dp = DealWithPwd()
MissionNum = "mmnn88"

urls = (
    '/', 'Index',
    '/index', 'Index',
    '/test', 'Test',
    '/login', 'Login',
    '/logout', 'Logout',
    '/faul', 'Faul',
    '/tables', 'Tables',
    '/charts', 'Charts',
    '/forms', 'Forms',
    '/up','Update',
    '/typography','Typo',
    '/post','PostD',
    '/test','Test',
    '/loginerror','LoginError',
    '/permission','Permission',
    '/upfile','UpFile',
    '/upcomplete','UpOver',
    '/logshow','LogShow',
    '/logget','LogGet',
    '/countapi', 'Countapi'
)

root = os.path.dirname(__file__)
render = web.template.render(os.path.join(root, "templates"))

allowed = (
    ('admin', '123123'),
    ('cuibing', '123123')
)

now_dir = os.path.split(os.path.realpath(__file__))[0]
db_dir = now_dir+"/db/log_daily.db"

class Countapi:
	def GET(self):
		apiname = web.input()
		dbconfig = config()
		dbpath = dbconfig.getvalue('db','sqlite_db')
		print dbpath
		if apiname['api']=='ecg' or apiname['api']=='run':
			api = apiTable(apiname['api']+'_api', dbpath)
			apiList = api.oprDB()
			if apiname['api']=='ecg':
				nameapi='ECG/SDK'
			else:
				nameapi = 'RUN'
			return render.SB_Admin.api(render.SB_Admin.allhead("Information-Support"), render.SB_Admin.navbar(session.username), render.SB_Admin.apiInfo(nameapi+'历史访问总排行',nameapi+'历史访问的api总排行',apiList))
			

def getlevel(username):

    level = {
        'admin':8,
        'cuibing':8,
        'show':2,
        'guest':1,
        'dev':3
    }
    return level.get(username)

web.config.debug = False
app = web.application(urls, globals())
#session = web.session.Session(app, web.session.DiskStore('sessions'),{'count': 0})
# 使用下面的代码可以处理掉debug模式不开启时重复加载session的问题
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), {'count': 0})
    # 这里利用count 来作为level的判断值
    web.config._session = session
else:
    session = web.config._session
### 调试添加

class Index:
    def GET(self):
        if session.get('logged_in', False):
            try:
                return render.SB_Admin.index(render.SB_Admin.allhead("Information-Support"), render.SB_Admin.navbar(session.username))
            except Exception, e:
                print "e" + str(e)
                return web.seeother('/faul')
        else:
            raise web.seeother('/login')
    def POST(self):
        # 首页4块post接口,4"nums" 1"line" 1"indexo" 2"tables"
        gdata = web.data()
        one1 = InitStr.switch_func(ConnPass.getone(gdata))
        return one1

class LogShow:
    def GET(self):
        if session.get('logged_in', False):
            try:
                if not session.logged_in:
                    return web.seeother('/login')
                elif session.level < 3:
                    return web.seeother('/permission')
                else:
                    return render.SB_Admin.logshow(render.SB_Admin.allhead("LogShow-Support"), render.SB_Admin.navbar(session.username))
            except Exception, e:
                print "e" + str(e)
                return web.seeother('/faul')
        else:
            raise web.seeother('/login')

    def POST(self):
        gdata = web.input()
        if gdata.get('gotnum', '2') == '1':
            # 返回查询数量
            eel = ExcuteErrLog()
            pdata = "%s" % eel.getnum()
        else:
            pdata = "null"
        return pdata

class LogGet:
    def POST(self):
        gdata = web.input()
        if gdata.get('gotlog', '2') == '1':
            # 返回日志
            el = ExcuteErrLog()
            pdata = "%s" % el.getlog(gdata.get('kind','null'))
        else:
            pdata = "null"
        return pdata

class LogBtn:
    def POST(self):
        gdata = web.input()
        if gdata.get('btn', '2') == '1':
            # 调用日志
            el = ExcuteErrLog()
            try:
                el.threadexcu()
            except ExcuteErrLog, e:
                errmsg = "func threadexcu_ %s" % str(e)
                log.writelog(errmsg)
            return 0
        else:
            return 9

class LogMail:
    def POST(self):
        gdata = web.input()
        if gdata.get('getmail', '2') == '1':
            el = ExcuteErrLog()
            el.sendmail(gdata.get('email', 'null'))
            return 1



class Faul:
    def GET(self):
        return render.SB_Admin.faul()

class Permission:
    def GET(self):
        return render.SB_Admin.permission()

class Test:
    def GET(self):
        return render.SB_Admin.test('cuibing', render.SB_Admin.allhead(), render.SB_Admin.navbar())

class Tables:
    def GET(self):
        if session.get('logged_in', False):
            try:
                if not session.logged_in:
                    return web.seeother('/login')
                elif session.level < 2:
                    return web.seeother('/permission')
                else:
                    return render.SB_Admin.tables(render.SB_Admin.allhead("urltables-Support"), render.SB_Admin.navbar(session.username))
            except Exception, e:
                print "e" + str(e)
                errmsg = "Class Table." + str(e)
                log.writelog(errmsg)
                return web.seeother('/faul')
        else:
            raise web.seeother('/login')

    def POST(self):
        date = web.data()
        return ConnPass.nginxpost(date)


class Typo:
    def GET(self):
        if session.get('logged_in', False):
            try:
                if not session.ip:
                    return web.seeother('/login')
                else:
                    return render.SB_Admin.typography()
            except Exception, e:
                print "e" + str(e)
                return web.seeother('/faul')
        else:
            raise web.seeother('/login')


class Charts:
    def GET(self):
        if session.get('logged_in', False):
            try:
                if not session.ip:
                    return web.seeother('/login')
                else:
                    return render.SB_Admin.charts(render.SB_Admin.allhead("char-Support"), render.SB_Admin.navbar(session.username))
            except Exception, e:
                print "e" + str(e)
                return web.seeother('/faul')
        else:
            raise web.seeother('/login')


class Forms:
    def GET(self):
        if session.get('logged_in', False):
            try:
                if session.ip and session.level > 7 :
                    return render.SB_Admin.forms(render.SB_Admin.allhead("Frame-Support"), render.SB_Admin.navbar(session.username))
                else:
                    return web.seeother('/permission')
            except Exception, e:
                print "e" + str(e)
                return web.seeother('/faul')
        else:
            raise web.seeother('/login')

class Update:
    def GET(self):
        if session.get('logged_in', False):
            try:
                if session.ip and session.level > 7 :
                    return render.SB_Admin.update(render.SB_Admin.allhead("Update-Support"), render.SB_Admin.navbar(session.username))
                else:
                    return web.seeother('/permission')
            except Exception, e:
                print "e" + str(e)
                return web.seeother('/faul')
        else:
            raise web.seeother('/login')

    def POST(self):
        got = web.input()
        if got.info2 == MissionNum:
            return 1
            #return "Have no Permission!"
        else:
            return 8

class UpFile:
    def POST(self):
        got = web.input()
        start = time.clock()
        if got.info2 == MissionNum and got.get('file', "pp") != "pp":
            wf = WriteFile('write_path', 'upfilepath')
            rc = wf.w_upfile(got.filename, got.file)
            end = time.clock()
            print ("Spend %f s.") %(end - start)
            if rc == 0:
                return 2
                #return "Receive file success.Begin to update..."
            else:
                return 7
        else:
            return 7

class UpOver:
    def POST(self):
        got = web.input()
        try:
            if got.pname:
                if up.thread_up(got.pname) == 5:
                    return 5
                else:
                    return 9
        except Exception, e:
            return 9
        else:
            return 9


class Login:
    def GET(self):
        return render.SB_Admin.login()

    def POST(self):
        i = web.input()
        username = i.get('username')
        passwd = i.get('password')
        if (username, dp.transmd5(passwd)) == dp.allowpwd(username):
            session.logged_in = True
            session.level = getlevel(username)
            session.username = username
            web.setcookie('system_mangement', '', 60)
            raise web.seeother('/')
        else:
            return web.seeother('/loginerror')

class LoginError:
    def GET(self):
        return render.SB_Admin.loginError()

    def POST(self):
        i = web.input()
        username = i.get('username')
        passwd = i.get('password')
        if (username, dp.transmd5(passwd)) == dp.allowpwd(username):
            session.logged_in = True
            session.level = getlevel(username)
            session.username = username
            web.setcookie('system_mangement', '', 60)
            raise web.seeother('/')
        else:
            return web.seeother('/loginerror')


class Logout:
    def GET(self):
        session.logged_in = False
        raise web.seeother("/login")


# main.py
def session_hook():
    web.ctx.session = session
    app.add_processor(web.loadhook(session_hook))


# views.py
class edit:
    def GET(self):
        try:
            session = web.ctx.session
            username = session.username
            if not username:
                return web.redirect('/login')
        except Exception as e:
            return web.redirect('/login')
        raise web.seeother('/login')


if __name__ == '__main__':
    # session_hook()
    app.run()
