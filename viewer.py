import tornado.web
import tornado.ioloop
import tornado.escape
import tornado.gen

from data_handler import index_handler as index
from data_handler import house_handler as house

app = tornado.web.Application([
    (r"/predict/", index.IndexHandler),
    (r"/predict/house/", house.HouseHandler),
])
