#!/usr/bin/env python
import webapp2

from handlers.auth import LoginHandler, LogoutHandler
from handlers.blog import NewPostHandler, BlogPostHandler, EditBlogPost
from handlers.contact import ContactHandler
from handlers.pages import MainHandler, AboutHandler, ForbiddenHandler

app = webapp2.WSGIApplication([
                                  webapp2.Route('/', MainHandler, name="main"),
                                  webapp2.Route('/about', AboutHandler, name="about"),
                                  webapp2.Route('/contact', ContactHandler),
                                  webapp2.Route('/login', LoginHandler),
                                  webapp2.Route('/logout', LogoutHandler),
                                  webapp2.Route('/new-post', NewPostHandler),
                                  webapp2.Route('/blog/<blog_id:\d+>/edit', EditBlogPost, name="blog-edit"),
                                  webapp2.Route('/forbidden', ForbiddenHandler, name="forbidden"),

                                  webapp2.Route('/blog/<slug:.+>', BlogPostHandler, name="blog-details"),
                              ], debug=True)
