__author__ = 'igorpodobnik'
import datetime


from google.appengine.ext import ndb

class Sporocilo(ndb.Model):
    vnos = ndb.StringProperty()
    nastanek = ndb.DateTimeProperty(auto_now_add=True)


class Forum(ndb.Model):
    fime = ndb.StringProperty()
    fpriimek = ndb.StringProperty()
    femail = ndb.StringProperty()
    fsporocilo = ndb.TextProperty()
    nastanek = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)
