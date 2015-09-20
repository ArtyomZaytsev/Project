import tornado.ioloop
import tornado.web
import pyorient

client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect("root", "network.ssl.keyStorePassword")
client.db_create( "my-project", pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_PLOCAL )