import tornado.ioloop
import tornado.web
import pyorient
import os, time

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    def get(self):
    	if not self.current_user:
            self.redirect("/login")
            return
        name = tornado.escape.xhtml_escape(self.current_user)
        self.write("Hello, " + name)     

class LoginHandler(BaseHandler):
    def get(self):
        self.render("index.html", title="My title")

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        if client.command("select @rid from Userdata where name = '%s' " % (self.get_argument("name"))):
        	self.write("This username is already taken, please try again") 
#        	self.redirect("/login")
        else: 
        	client.command( 'CREATE VERTEX Userdata set name = "%s", password = "%s"' % (self.get_argument("name"), self.get_argument("password")) )
        	self.redirect("/")

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret" : "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/login", LoginHandler),
	], **settings)


client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect( "root", "network.ssl.keyStorePassword" )
if not client.db_exists( "my-project", pyorient.STORAGE_TYPE_PLOCAL ):
	client.db_create( "my-project", pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_PLOCAL )
client.db_open( "my-project", "root", "network.ssl.keyStorePassword" )

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.current().start()


    #создать соединение (вебсокет, база)
    #предложить базовую архитектуру (как хранятся пользователи, проекты, как будут взаимодействать)
    #базовая структура представления проекта
    -создавать пользователя(редакт, удал)
    -список пользователей