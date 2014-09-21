import time
import json
import logging
import tornado.web


class RestHandler(tornado.web.RequestHandler):
    """ To be inherited by other handlers """

    model = None

    def set_custom_headers(self):
        """ Set some custom and security related headers """
        # self.set_header('x-frame-options', 'DENY')
        # self.set_header('x-xss-protection', '1; mode=block')
        self.set_header('Access-Control-Allow-Origin', '*')

    def prepare(self):
        super(RestHandler, self).prepare()
        self.set_custom_headers()

    def write_json(self, data, status_code=200):
        """ Write json data to the client """
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.set_status(status_code)
        self.write(json.dumps(data))

    def get(self, key=None):
        """ Get resource """
        if key:
            item = self.model.get(key)
            if item:
                self.write_json(item)
            else:
                raise tornado.web.HTTPError(404)
        else:
            items = self.model.all()
            self.write_json(items)

    def post(self, _=None):
        """ Create a new resource """
        data = json.loads(self.request.body.decode('utf-8'))
        item = self.model.new(data)
        self.write_json(item)

    def delete(self, key=None):
        """ Delete an resource """
        self.model.delete(key)
        self.set_status(204)
