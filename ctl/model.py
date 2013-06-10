#!/usr/bin/env python
# created by jiango @2013.6
#

from google.appengine.ext import db

class articleType(db.Model):
	typeName = db.StringProperty()
	articleCount = db.IntegerProperty()

class article(db.Model):
    title = db.StringProperty()
    content = db.StringProperty()
    postime = db.DateTimeProperty()
    readCount = db.IntegerProperty()
    commentCount  = db.IntegerProperty()

#class topArticle(article):
#    slidePhoto = db.StringProperty()

class misc(db.Model):
	pass

class articleDo(object):
	def dele(self, key):
		db.delete(key)
	def get(self, key):
		return db.get(key)



