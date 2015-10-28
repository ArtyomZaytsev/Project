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
        self.render("index.html")

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        print clients
        users = db.query("select name, age, city from Userdata LIMIT 1000")
        self.get_users_info(users)
        self.write_message("Usr_empty")

    def on_message(self, message):
        if message.startswith("usrdata_"):
            usrdata = message.split('*****')
            usrdata[0] = usrdata[0][8:]
            if self.is_user_empty(usrdata):
                self.write_message("Usr_alr_taken")
            else:
                self.create_user(usrdata)
        elif message.startswith("usrinfo_"):
            self.edit_user(message)

        else:
            pass
 
    def on_close(self):
        print 'connection closed'
 
    def check_origin(self, origin):
        return True

    def is_user_empty(self, usrdata):
        return db.command("select @rid from Userdata where name = '%s' " % usrdata[0])

    def create_user(self, usrdata):
        db.command( 'CREATE VERTEX Userdata set name = "%s", password = "%s"' % (usrdata[0], usrdata[1]) )
        clients[self] = usrdata[0]
        main_user_info = db.query('select name, age, city from Userdata where name = "%s"' % clients[self])
        self.get_users_info(main_user_info, True)
        users_info = db.query("select name, age, city from Userdata LIMIT 1000")
        self.get_users_info(users_info)

    def get_users_info(self, users, main_usr=False):
        for i in users:
            user = {}
            user_to_send = {}
            user['name'] = i.oRecordData['name']
            if i.oRecordData.get('age'):
                user['age'] = i.oRecordData['age']
            if i.oRecordData.get('city'):
                user['city'] = i.oRecordData['city']
            if main_usr:
                user_to_send['Main_usr_info'] = user
            else:
                user_to_send['Usrs_info'] = user
            self.write_message(json.dumps(user_to_send))

    def edit_user(self, message):
        usrdata = message.split('***')
        usrdata[0] = usrdata[0][8:]
        db.command( 'update Userdata set name="%s", age="%s", city="%s" where name="%s"' % (usrdata[0], usrdata[1], usrdata[2], clients[self]) )
        user_info = db.query('select name, age, city from Userdata where name = "%s"' % usrdata[0])
        self.get_users_info(user_info, True)
        users_info = db.query("select name, age, city from Userdata LIMIT 1000")
        self.get_users_info(users_info)

settings = {
    'template_path': 'templates',
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret" : "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r'/ws', WSHandler),
    ], **settings)

 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Websocket Server Started at %s***') % myIP
    tornado.ioloop.IOLoop.instance().start()