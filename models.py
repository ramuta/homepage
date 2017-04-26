from google.appengine.ext import ndb

__author__ = 'matej'


class BlogPost(ndb.Model):
    title = ndb.StringProperty()
    slug = ndb.StringProperty(default="none")
    text = ndb.TextProperty()
    author = ndb.StringProperty(indexed=False)
    datetime = ndb.DateTimeProperty(auto_now_add=True)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, title, slug, text):
        post = cls(title=title,
                   slug=slug,
                   text=text,
                   author="Matt Ramuta")
        post.put()

    @classmethod
    def update(cls, blog_post, title=None, slug=None, text=None):
        if title:
            blog_post.title = title

        if slug:
            blog_post.slug = slug

        if text:
            blog_post.text = text

        blog_post.put()
        return blog_post
