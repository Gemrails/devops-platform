import base64

s = "123456"

#t = raw_input(input pwd:)

a = base64.b64encode(s)

mm = 'bUhlYWx0aDEyMw=='

#b = base64.b64encode(t)

b = base64.decodestring(a)

print a 
print b

if a == b:
    pass
else:
    try:
        errmsg = "Not equal."
        raise
    except Exception, e:
        print str(e)
