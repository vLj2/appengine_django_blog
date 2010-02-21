#from django.db import models
# Create your models here.


from appengine_django.models import BaseModel
from google.appengine.ext import db

class BlogPost(BaseModel):
    title = db.StringProperty()
    uri = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    teaser = db.TextProperty()
    teaser_html = db.TextProperty()
    content = db.TextProperty()
    content_html = db.TextProperty()
    tags = db.StringProperty()

