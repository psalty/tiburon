import datetime
from google.appengine.ext import db
import logging
from ImageBlob import ImageBlob, create_image_blob

def get_review_key(review_name=None):
    return db.Key.from_path('Reviews', review_name or 'default_review')

"""
    Class Venue
    name : Name of Venue
    Address : Address of Venue
    ophour : operation hour of Venue.
    geotag : geo location of venue. (read only. when Address entered, it will be updated accordingly). Google Geo Coding API
    contact : contact information
    website : optional
    menu : list of Food Item Keys that the Venue is serving
    Srating : service rating 
    Trating : Traffic rating . How congested the venue is.
    Crating : Cleaness rating
    status : the existence of venue
    origin : nationality of venue
"""
class Venue(db.Model):
    name = db.StringProperty()
    address = db.StringProperty()
    ophour  = db.StringProperty()
    geotag  = db.GeoPtProperty()
    contact = db.StringProperty()
    website = db.URLProperty()
    menu    = db.ListProperty(db.Key)
    Srating = db.RatingProperty()
    Trating = db.RatingProperty()
    Crating = db.RatingProperty()
    status  = db.BooleanProperty()
    origin  = db.CategoryProperty()

                
"""
    Class Dish
    style : type of food
"""
class Dish(db.Model):
    name    = db.StringProperty()
    style   = db.CategoryProperty()

"""
    Class Tuple
    {dish, venue} tuple
    Trating : Taste rating
    Arating : Amount rating
    Prating : Price rating
    status : the validity of food item
"""
class Tuple(db.Model):
    date    = db.DateTimeProperty(auto_now_add=True)
    venue   = db.ReferenceProperty(Venue, None, 'venue')
    dish    = db.ReferenceProperty(Dish, None, 'dish')
    image   = db.ReferenceProperty(ImageBlob,None,'image')
    Trating = db.RatingProperty()
    Arating = db.RatingProperty()
    Prating = db.RatingProperty()
    status  = db.BooleanProperty()
    def update_my_image(self, img):
        if  img:
            self.image = create_image_blob(img)
            self.put()
            
    
def add_new_review(food_item, place, pic):
    group_name = get_review_key()
    new_venue   = Venue(parent = group_name)
    new_venue.name = place
    new_venue.put()
    new_dish    = Dish(parent = group_name)
    new_dish.name = food_item
    new_dish.put()
    new_tuple = Tuple(parent = group_name)
    new_tuple.venue = new_venue.key()
    new_tuple.dish = new_dish.key()
    
    new_tuple.put()

    if pic:
        new_tuple.update_my_image(pic)
