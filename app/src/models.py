import base64
import bson
import time
import gridfs
import pymongo
import logging
from PIL import Image as Img
import io

con = pymongo.Connection()
database = con['vocaleyesdb']
col = database['items']
grid = gridfs.GridFS(database)


class Default(object):
    """ A resource """

    @classmethod
    def new(cls, item):
        """ Create a new item in the database """
        key = col.insert(item)
        item['_id'] = str(key)
        return item

    @classmethod
    def all(cls, limit=100, offset=0):
        """ Return all items """
        return cls.find({}, limit, offset)

    @classmethod
    def get(cls, key):
        """ Return item by key """
        item = col.find_one({'_id': bson.ObjectId(key)})
        if item:
            item['_id'] = str(item['_id'])
        return item

    @classmethod
    def find(cls, kwargs, limit=100, offset=0, sort=None):
        """" Find an item based on certain criteria """
        sort = sort or ('_id', pymongo.DESCENDING)
        items = col.find(kwargs).limit(limit).skip(offset).sort(*sort)
        results = []
        for item in items:
            item['_id'] = str(item['_id'])
            img_id = item.get('image', {}).get('_id')
            th_img_id = item.get('image', {}).get('_th_id')
            if img_id:
                item['image']['url'] = \
                    'http://vocaleyesapp.org/v1/images/{}'.format(img_id)
            if th_img_id:
                item['image']['th_url'] = \
                    'http://vocaleyesapp.org/v1/images/{}'.format(th_img_id)
            results.append(item)
        return results


class Item(Default):

    @classmethod
    def new(cls, item):
        """ Create a new item in the database """

        def create_image(_bytes, **kwargs):
            """ Create an image on the grid """
            _id = grid.put(bytes_, **kwargs)
            return str(_id)

        def create_thumbnail(_bytes, **kwargs):
            """ Create thumbnail """
            in_ = io.BytesIO(_bytes)
            im = Img.open(in_)
            im.thumbnail((72, 72), Img.ANTIALIAS)
            out = io.BytesIO()
            im.save(out, "JPEG")
            out.seek(0)
            _id = grid.put(out, **kwargs)
            return str(_id)

        image_data = item['image'].pop('base64data')
        bytes_ = base64.b64decode(image_data)
        item['image']['_id'] = create_image(bytes_)
        item['image']['_th_id'] = create_thumbnail(bytes_)
        item['timestamp'] = int(time.time())
        key = col.insert(item)

        item['_id'] = str(key)
        return item


class User(Default):
    pass


class Image(Default):
    """ The image stored on the GridFS """

    @classmethod
    def get(cls, key):
        return grid.get(bson.ObjectId(key))
