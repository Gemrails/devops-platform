#!/usr/bin/env python
# coding: utf-8
import web
from web import form
import os
import webmain


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

if __name__ == '__main__':
    # session_hook()
    app.run()
