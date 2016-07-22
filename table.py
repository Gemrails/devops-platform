#/usr/bin/python
#coding=utf-8

import web
import webmain

'''
class Tables:

    def GET(self):
        if session_hook().get('logged_in', False):
            try:
                if not session_hook().ip:
                    return web.seeother('/login')
                else:
                    return webmain.render.SB_Admin.tables()
            except Exception, e:
                print "e" + str(e)
                return web.seeother('/fasle')
        else:
            raise web.seeother('/login')
'''


def session_hook():
    #session = \
    web.ctx.session = session
app.add_processor(web.loadhook(session_hook))
