import webapp2
import jinja2
import os
import logging
import json
from google.appengine.ext import db
from datamodel import add_new_review
from datamodel import get_review_key

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader([os.path.dirname(__file__), 'html']))
debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

xg_on = db.create_transaction_options(xg=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        tuples = db.GqlQuery("SELECT * "
                            "FROM Tuple "
                            "WHERE ANCESTOR IS :1 "
                            "LIMIT 10",
                            get_review_key())
        logging.debug("*******************")
        for i in tuples:
            if i.image:
                logging.debug(i.image.key())
            
        template_values = {
                           'items' : tuples,
                           }
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

class CreateNewEntry(webapp2.RequestHandler):
    def post(self):
        food    = self.request.get("food")
        venue   = self.request.get("venue")
        pic     = self.request.get('review_pic')
            
            
        if food == None or venue == None:
            self.response.out.write(json.dumps({ 'status' : 'NOK' , 'Cause' : 'Food or Venue is None'}))
        else:
            db.run_in_transaction_options(xg_on, add_new_review , food, venue, pic)
            self.redirect('/')

class Image(webapp2.RequestHandler):
    def get(self):
        imgtype = self.request.get("type")
        logging.debug("dsfsdffffffffffffffffffffffff")
        logging.debug(self.request.get("gkey"))
        try:
            image = db.get(self.request.get("gkey"))
        except:
            self.response.out.write("No image")
            return
        
        if image:
            self.response.headers['Content-Type'] = "image/png"
            if imgtype == 'thumb':
                self.response.out.write(image.thumb)
            elif imgtype == 'medium':
                self.response.out.write(image.medium)
            else:
                self.response.out.write(image.img_src)
        else:
            self.response.out.write("No image")

application_paths = [('/', MainPage),
                     ('/create', CreateNewEntry),
                     ('/img',Image),
                    ]

app = webapp2.WSGIApplication(application_paths, debug=debug)


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    app.run()

if __name__ == '__main__':
    main()
