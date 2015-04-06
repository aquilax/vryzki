from google.appengine.ext import db
from google.appengine.ext import search

__author__="aquilax"
__date__ ="$Feb 20, 2010 8:15:35 AM$"


class MyNode(db.Model):
  name = db.StringProperty(verbose_name="Name")
  search = db.StringProperty(verbose_name="Name")
  created = db.DateTimeProperty(verbose_name="Addred", auto_now_add=True)
  status = db.IntegerProperty(default=1)

class MyAction(db.Model):
  name = db.StringProperty(verbose_name="Name")
  search = db.StringProperty(verbose_name="Name")
  created = db.DateTimeProperty(verbose_name="Addred", auto_now_add=True)
  status = db.IntegerProperty(default=1)
  
class MyVertice(db.Model):
  left = db.ReferenceProperty(MyNode, collection_name="left")
  right = db.ReferenceProperty(MyNode, collection_name="right")
  action = db.ReferenceProperty(MyAction)
  created = db.DateTimeProperty(verbose_name="Addred", auto_now_add=True)
  ref = db.StringProperty(verbose_name="URL")
  dfrom = db.StringProperty(verbose_name="From")
  dto = db.StringProperty(verbose_name="To")
  status = db.IntegerProperty(default=1)

def ps(text):
  return text.strip().lower().replace(' ', '')

def getnode(nname):
  q = MyNode.all()
  q.filter("search =", ps(nname))
  results = q.fetch(1)
  if results:
    return results[0]
  else:
    node = MyNode()
    node.name = nname
    node.search = ps(nname)
    node.put()
    return node

def getaction(nname):
  q = MyAction.all()
  q.filter("search =", ps(nname))
  results = q.fetch(1)
  if results:
    return results[0]
  else:
    action = MyAction()
    action.name = nname
    action.search = ps(nname)
    action.put()
    return action

def save(data):
  left = data.get('left')
  right = data.get('right')
  action = data.get('action')
  dfrom = data.get('dfrom')
  dto = data.get('dto')
  ref = data.get('ref')
  
  vert = MyVertice();
  vert.left = getnode(left)
  vert.right = getnode(right)
  vert.action = getaction(action)
  vert.dfrom = dfrom
  vert.dto = dto
  vert.ref = ref
  vert.put()

def searchnode(text):
  return MyNode.all().search(text).fetch(10)

def searchaction(text):
  return MyAction.all().search(text).fetch(10)