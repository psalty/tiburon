'''
Created on May 26, 2012

@author: jaehong park
@email : psalty@gmail.com
'''
from google.appengine.ext import db

class OriginTags(db.Model):
    tag = db.CategoryProperty()
    cnt = db.IntegerProperty()
    
class StyleTags(db.Model):
    tag = db.CategoryProperty()
    cnt = db.IntegerProperty()
    
def update_origin_tagcounter(kw):
    newtags = OriginTags.gql("WHERE tag =:1",kw)
    newTag = newtags.get()
    if newTag:
        newTag.cnt +=1;
    else:
        newTag = OriginTags()
        newTag.cnt = 1;
        newTag.tag = kw
    newTag.put()

def remove_oritin_tagcounter(tag):
    oldtags = OriginTags.gql("WHERE tag =:1",tag)
    oldTag = oldtags.get()
    if oldTag:
        oldTag.cnt -=1;
        if oldTag.cnt == 0:
            oldTag.delete()
        else:
            oldTag.put()

def update_style_tagcounter(kw):
    newtags = StyleTags.gql("WHERE tag =:1",kw)
    newTag = newtags.get()
    if newTag:
        newTag.cnt +=1;
    else:
        newTag = StyleTags()
        newTag.cnt = 1;
        newTag.tag = kw
    newTag.put()

def remove_style_tagcounter(tag):
    oldtags = StyleTags.gql("WHERE tag =:1",tag)
    oldTag = oldtags.get()
    if oldTag:
        oldTag.cnt -=1;
        if oldTag.cnt == 0:
            oldTag.delete()
        else:
            oldTag.put()