import tornado.web
from src.handlers import MainHandler, BrowseHandler
from src.handlers import ItemRestHandler, ImageRestHandler, ItemViewHandler
from src.handlers import RecentHandler

routes = [
    (r'/', MainHandler),
    (r'/recent', RecentHandler),
    (r'/browse', BrowseHandler),
    (r'/items/?(.+)?', ItemViewHandler),
    (r'/static/(.+)', tornado.web.StaticFileHandler),
    (r'/v1/items/?(.+)?', ItemRestHandler),
    (r'/v1/images/?(.+)?', ImageRestHandler),
]
