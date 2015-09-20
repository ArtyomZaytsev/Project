import tornado.ioloop
import tornado.web
import pyorient

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", MainHandler),
])

#client = pyorient.OrientDB("localhost", 2424)
#session_id = client.connect("root", "network.ssl.keyStorePassword")
#client.db_create( "my-project", pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY )

if __name__ == "__main__":
    application.listen(3000)
    tornado.ioloop.IOLoop.current().start()
    

