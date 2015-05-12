#--------------------------------Hello World----------------------------------------------------
from klein import Klein
app = Klein()

@app.route('/Hello')
def hello(request):
    return 'Hello, world!'


#-----------------------------------------Adding Routes----------------------------------------------

@app.route('/AR')
def pg_root(request):
	return 'I am the root page!'

#@app.route('/about')
#def pg_about(request):
		#return 'I am Klein application'

#app.run("localhost", 8080)

#-----------------------------------------Variable Routes----------------------------------------------

@app.route('/VR/<username>')
def pg_VR(request, username):
    return 'Hi %s!' % (username,)


#from klein import Klein
#app = Klein ()

#@app.route('/<string:arg>')
#def pg_string(request, arg):
	#return 'String: %s!' %(arg,)

#@app.route('/<int:arg>')
#def pg_int(request, arg):
	#return 'int: %s!' %(arg,)
#@app.route('/<float:arg>')
#def pg_float(request, arg):
	#return 'Float: %s!' %(arg,)

#app.run("localhost", 8080) 

#-----------------------------------------Route Order Matters---------------------------------------------

#@app.route('/user/<username>')
#def pg_user(request, username):
    #return 'Hi %s!' % (username,)

@app.route('/ROM/bob')
def pg_user_bob(request):
    return 'Hello there bob!'



#-----------------------------------------Static Files---------------------------------------------------

#from twisted.web.static import File 

#from klein import Klein
#app = Klein()

#@app.route('/',branch = True)
#def pg_index(request):
	#return File ('./')

#app.run("localhost", 8080)

#-----------------------------------------Deferreds---------------------------------------------------
#import treq
#from klein import Klein
#app = Klein()

#@app.route('/', branch=True)
#def google(request):
    #d = treq.get('https://www.google.com' + request.uri)
    #d.addCallback(treq.content)
    #return d

#app.run("localhost", 8080)