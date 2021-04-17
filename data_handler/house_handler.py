import sys
import os
import json
import tornado.escape

sys.path.append(os.pardir)

class HouseHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.set_header('Access-Control-Allow-Methods', 'OPTIONS,POST')

    def get(self):
        data={}
        try:
            header= self.request.headers.get('data')
            data = json.loads(header)
        except:
            _, ms, _ = sys.exc_info()
            message = "Error Message:{0}".format(ms)
            self.write(message)
        try:
            # TODO:파라미터 넘겨서 집 값 예측
            address = data['address']
            json_data = json.dumps(address)
            self.write(json_data)
        except:
            _, ms, _ = sys.exc_info()
            message = "Error Message:{0}".format(ms)
            self.write(message)
            pass
