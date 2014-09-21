import time
import json
import logging
import tornado.web

from app.src.models import Item, User, Image
from app.src.rest import RestHandler


class BaseHandler(tornado.web.RequestHandler):
    """ To be inherited by other handlers """

    def set_custom_headers(self):
        """ Set some custom and security related headers """
        # self.set_header('x-frame-options', 'DENY')
        # self.set_header('x-xss-protection', '1; mode=block')
        self.set_header('Access-Control-Allow-Origin', '*')

    def prepare(self):
        super(BaseHandler, self).prepare()
        self.set_custom_headers()

    def write_json(self, data, status_code=200):
        """ Write json data to the client """
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.set_status(status_code)
        self.write(json.dumps(data))


class MainHandler(BaseHandler):
    def get(self):
        self.render('index.html')


class ItemRestHandler(RestHandler):
    """ Rest handler for the main resource """
    model = Item


class AccountRestHandler(RestHandler):
    """ Rest handler for the main resource """
    model = User


class BrowseHandler(RestHandler):
    """ Rest """

    def get(self):
        items = Item.all()
        self.render('browse.html', items=items)


class ImageRestHandler(BaseHandler):

    def get(self, key=None):
        if not key:
            raise tornado.web.HTTPError(404)

        fh = Image.get(key)
        if not fh:
            raise tornado.web.HTTPError(404)
        else:
            self.set_header('Content-Type', 'image/jpeg')
            self.write(fh.read())


class ItemViewHandler(ItemRestHandler):
    def get(self, key):
        if not key:
            raise tornado.web.HTTPError(404)
        item = self.model.get(key)
        if item:
            self.render('card.html', item=item)
        else:
            raise tornado.web.HTTPError(404)


class RecentHandler(ItemRestHandler):
    def get(self):
        since = int(self.get_argument('since'))
        items = self.model.find({'timestamp': {'$gt': since}})
        self.write_json(items)
