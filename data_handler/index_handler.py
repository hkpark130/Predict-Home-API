import sys
import os
import json
import tornado.escape

sys.path.append(os.pardir)

class IndexHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.set_header('Access-Control-Allow-Methods', 'OPTIONS,GET')

    def get(self):
        try:
            self.write('hello')
        except:
            _, ms, _ = sys.exc_info()
            message = "Error Message:{0}".format(ms)
            self.write(message)
