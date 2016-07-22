#!/usr/bin/python
#coding=utf8

import paramiko
import web
import os
import commands
from switch import switch_ip, switch_pwd, switch_username


root = os.path.dirname(__file__)
print os.path.join(root,'templates')
#print os.path.join(root, 'templates/')
render = web.template.render(os.path.join(root, 'templates'))
'''
    此处无法写成相对路径,需用此方法获得绝对路径.
'''
print render
#render = web.template.render('templates/')

web.config.debug = False

urls = (
    '/', 'index',
    #'/pet', 'pet',
    '/login','Login',
)

allowed = (
	('admin','123123'),
)

app = web.application(urls, locals())

session = web.session.Session(app, web.session.DiskStore('sessions'))

def getfile(filepath):

    #执行部分
    ssh = paramiko.SSHClient()
    comm = 'ls '+filepath
    print comm

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,PORT,username,passwd,timeout=10)
    stdin, stdout, stderr = ssh.exec_command(comm)
    stdin.write("Yes")
    out = stdout.readlines()
    ssh.close()
    print out
    return out

def format_file(filepath, filelist):

    list = ""
    for f in filelist:
        list += filepath+'/'+f +'\n'
    #return list
    return filelist



class checkfile():

    def __init__(self, filepath):

        self.filepath = filepath

    def catfile(self, num = 10):

        tail_log = "tail -n %d %s" %(num, self.filepath)
        #content = os.popen(tail_log)
        (status, output) = commands.getstatusoutput(tail_log)
        print output
        return output

    def get_file(self, servername):

        PORT = 22
        localpath = '/Users/pujielan/Documents/chetest/'    # 安装时创建一下个默认目录
        Username = switch_username(servername)
        #print Username
        passwd = switch_pwd(servername)
        filename = self.filepath.split("/")[-1]
        ip =  switch_ip(servername)
        trans = paramiko.Transport(ip, PORT)
        try:
            trans.connect(username = Username, password = passwd)
            sftp = paramiko.SFTPClient.from_transport(trans)
            src = self.filepath
            #print src
            des = localpath + filename
            #print des
            sftp.get(src,des)
            trans.close()
            return des
        except Exception, e:
            print "get_phpcode" + str(e)
            trans.close()
            return
        pass


class index:


    def GET(self):
        if session.get('logged_in',False):
            return '<h1>Login Success!!!</h1><a href="/test">test</a></br><a href="/logout">Logout</a>'
        raise web.seeother('/login')
    '''
    def GET(self,name):

        print name
        if not name:
            filelist = format_file("/root/", getfile("/root"))
        else:
            filelist = format_file("/root/"+name, getfile("/root/"+name))
        #return filelist
        return render.index(filelist,name)

        #return "Hello, world!" + filename
    '''

'''
class pet:

    def GET(self, name):
        name = "pet care"
        print name
        return render.temp1.html(name)
'''


class Login():
    def __init__(self):
        pass

    def GET(self):
        return render.login()

    def POST(self):
        i = web.input()
        username = i.get('username')
        password = i.ger('password')
        if (username, password) in allowed:
            session.logged_in = True
            web.setcookie('system_mangement', '', 60)
            raise web.seeother('/')
        else:
            return '<h1>Login Error!!!</h1></br><a href="/login">Login</a>'


#main.py
def session_hook():
    web.ctx.session = session
    app.add_processor(web.loadhook(session_hook))

#views.py
class edit:
    def GET(self):
        try:
            session = web.ctx.session
            username = session.username
            if not username:
                return web.redirect('/login')
        except Exception as e:
            return web.redirect('/login')
        #return render_template('edit.html')


if __name__ == "__main__":
    #getfile()
    #app = web.application(urls, globals())
    app.run()
    #check1 = checkfile("/root/install.log")
    #check1.catlog()
    #check1.cat_phpcode("test")
    #check2 = checkfile(check1.get_file('test'))
    #check2.catfile(1)




