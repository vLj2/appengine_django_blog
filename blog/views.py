# Create your views here.

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.db import djangoforms

import re
import markdown

import django
from django import shortcuts
from django import http
from django import template


from blog.models import BlogPost


# to slugify URLs:
register = template.Library()

@register.filter
def slugify(string):
    string = re.sub('\s+', '_', string)
    string = re.sub('[^\w.-]', '', string)
    return string.strip('_.- ').lower()


# to use Django's form libraries to build create/edit forms from the BlogPost model
class BlogPostForm(djangoforms.ModelForm):
  class Meta:
    model = BlogPost
    exclude = ['uri', 'date', 'teaser_html', 'content_html']



def index(request):
    """Displays the index page."""
    # Fetch all of the BlogPosts
    posts = BlogPost.all().order('-date')

    # Setup the data to pass on to the template
    template_values = {
        'posts': posts,
    }

    # Load and render the template
    return shortcuts.render_to_response('index.html', template_values)

def view(request, post_uri):
    # Find the requested post
    post = BlogPost.all().filter('uri = ', post_uri).fetch(1)

    # Make sure the requested post exists
    if post == None or len(post) == 0:
        return http.HttpResponseNotFound('No post exists with that uri (%r)' % post_uri)

    # Get the requested post data
    post = post[0]

    # Load and display the view template
    return shortcuts.render_to_response('view.html', {'post': post})



def create(request):
    """Displays the BlogPost create form."""
    # Fetch the current user
    user = users.get_current_user()

    # Make sure someone is logged in
    if user == None:
        return http.HttpResponseRedirect(users.create_login_url(request.path))
    # Make sure the user is an admin
    if users.is_current_user_admin() != True:
        return http.HttpResponseRedirect('/blog/')

    form = BlogPostForm(data=request.POST)

    if not request.POST:
        # If the user makes it this far then display the create form
        return shortcuts.render_to_response('create.html', {'form': form})

    errors = form.errors
    post = None
    if not errors:
        try:
            post = form.save(commit=False)
        except ValueError, err:
            errors['__all__'] = unicode(err)
    if errors:
        # There were errors, redisplay the create form
        return shortcuts.render_to_response('create.html', {'form': form})

    # Setup Markdown with the code highlighter
    md = markdown.Markdown(extensions=['codehilite'])

    # Convert the teaser and content Markdown into html
    post.teaser_html = md.convert(post.teaser)
    post.content_html = md.convert(post.content)

    # Build the URI slug from the post title
    post.uri = slugify(post.title)

    # Check to see if we should only preview the post
    if (request.POST['submit'] == 'Preview'):
        # Re-display the create form with the post preview
        return shortcuts.render_to_response('create.html', {'form': form, 'preview':post})

    # If we made it this far then we should save the post to the DB
    post.put()

    return http.HttpResponseRedirect('/')

