import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import os

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader("./templates")
        self.write(loader.load("ws.html").generate())

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
    
    def on_message(self, message):
        if message.startswith("user_"): 
            self.write_message('this is user: ' + message[5:])
        elif message.startswith("pwd_"): 
            self.write_message('this is password: ' + message[4:])
        else:
            pass
 
    def on_close(self):
        print 'connection closed'
 
    def check_origin(self, origin):
        return True
 
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