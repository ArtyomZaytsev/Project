import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import pyorient
import socket
import json
import os

clients = {}

db = pyorient.OrientDB("localhost", 2424)
session_id = db.connect( "root", "network.ssl.keyStorePassword" )
if not db.db_exists( "my-project", pyorient.STORAGE_TYPE_PLOCAL ):
    db.db_create( "my-project", pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_PLOCAL )
db.db_open( "my-project", "root", "network.ssl.keyStorePassword" )

class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("login.html")

class ProfileHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("profile.html")

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        print clients
    
    def on_message(self, message):
        if message.startswith("usrdata_"):
            usrdata = message.split('*****')
            usrdata[0] = usrdata[0][8:]
            if db.command("select @rid from Userdata where name = '%s' " % usrdata[0]):
                self.write_message("This username is already taken, please try again")
            else:
                db.command( 'CREATE VERTEX Userdata set name = "%s", password = "%s"' % (usrdata[0], usrdata[1]) )
                clients[self] = usrdata[0]
                print clients
                self.write_message("ok")
        elif message.startswith("editusr_"):
            self.write_message(clients[self])
        elif message.startswith("usrlist_"):
            userlist = self.get_users()
            self.write_message(json.dumps(userlist))
        else:
            pass
 
    def on_close(self):
        print 'connection closed'
 
    def check_origin(self, origin):
        return True

    def get_users(self):
        users = db.query("select name from Userdata")
        for i in range(len(users)):
            users[i] = users[i].oRecordData['name']
        return users

settings = {
    'template_path': 'templates',
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret" : "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r'/ws', WSHandler),
    (r"/profile", ProfileHandler),
    ], **settings)

 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Websocket Server Started at %s***') % myIP
    tornado.ioloop.IOLoop.instance().start()