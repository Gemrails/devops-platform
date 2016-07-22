#!/usr/bin/env python
# coding: utf-8
import web
from web import form
import os
import dealwith_http_log
import read_ini

urls = (
    '/', 'Index',
    '/index', 'Index',
    '/test', 'Test',
    '/login', 'Login',
    '/logout', 'Logout',
    '/false', 'F404',
    '/tables', 'Tables',
    '/charts', 'Charts',
    '/forms', 'Forms',
    '/up','Update',
    '/typography','Typo',
    '/loginerror','LoginError'
)

root = os.path.dirname(__file__)
render = web.template.render(os.path.join(root, "templates"))

allowed = (
    ('admin', '123123'),
)

web.config.debug = False
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'))


class Index:
    def GET(self):
        if session.get('logged_in', False):
            try:
                if not session.ip:
                    return web.seeother('/login')
                else:
                    return render.SB_Admin.index()
            except Exception, e:
                print "e" + str(e)
                return web.seeother('/fasle')
        else:
            raise web.seeother('/login')


class F404:
    def GET(self):
        return render.F404()



class Tables:
    def GET(self):
        if session.get('logged_in', False):
            try:
                if not session.ip:
                    return web.seeother('/login')
                else:
                    return render.SB_Admin.tables()
            except Exception, e:
                print "e" + str(e)
                return web.seeother('/fasle')
        else:
            raise web.seeother('/login')

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
                return web.seeother('/fasle')
        else:
            raise web.seeother('/login')


class Charts:
    def GET(self):
        if session.get('logged_in', False):
            try:
                if not session.ip:
                    return web.seeother('/login')
                else:
                    return render.SB_Admin.charts()
            except Exception, e:
                print "e" + str(e)
                return web.seeother('/fasle')
        else:
            raise web.seeother('/login')


class Forms:
    def GET(self):
        if session.get('logged_in', False):
            try:
                if not session.ip:
                    return web.seeother('/login')
                else:
                    return render.SB_Admin.forms()
            except Exception, e:
                print "e" + str(e)
                return web.seeother('/fasle')
        else:
            raise web.seeother('/login')

class Update:
    def GET(self):
        if session.get('logged_in', False):
            try:
                if not session.ip:
                    return web.seeother('/login')
                else:
                    return render.SB_Admin.update()
            except Exception, e:
                print "e" + str(e)
                return web.seeother('/fasle')
        else:
            raise web.seeother('/login')

class Login:
    def GET(self):
        return render.SB_Admin.login()

    def POST(self):
        i = web.input()
        username = i.get('username')
        passwd = i.get('password')
        if (username, passwd) in allowed:
            session.logged_in = True
            #
            # session_hook()
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
        if (username, passwd) in allowed:
            session.logged_in = True

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
