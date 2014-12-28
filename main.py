#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
from google.appengine.api import mail, users
import jinja2
import webapp2
from decorators import login_required
from models import BlogPost
from secret import emails
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

import markdown2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               extensions=['jinja2.ext.autoescape'],
                               autoescape=False)


class Handler(webapp2.RequestHandler):
    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        user = users.get_current_user()
        if user:
            email = user.email()
            if email in emails:
                params["hello"] = "Hello, Matej"
        t = jinja_env.get_template(view_filename)
        self.write(t.render(params))


class MainHandler(Handler):
    def get(self):
        posts = BlogPost.query().order(-BlogPost.datetime).fetch()

        # convert markdown to html
        posts2 = []
        markdowner = markdown2.Markdown()

        for post in posts:
            post.text = markdowner.convert(post.text)
            posts2.append(post)

        params = {"posts": posts2}
        self.render_template('index.html', params)


class AboutHandler(Handler):
    def get(self):
        self.render_template('about.html')


class ForbiddenHandler(Handler):
    def get(self):
        self.render_template('403.html')


class NewPostHandler(Handler):
    @login_required
    def get(self):
        return self.render_template('newpost.html')

    @login_required
    def post(self):
        title = self.request.get("title")
        slug = self.request.get("slug")
        text = self.request.get("text")
        BlogPost.create(title, slug, text)
        return self.redirect_to("main")


class ContactHandler(Handler):
    def get(self):
        self.render_template('contact.html')

    def post(self):
        sender = self.request.get("sender")
        subject = self.request.get("subject")
        email = self.request.get("email")
        text = self.request.get("text")
        hidden = self.request.get("hidden")
        if hidden:
            return self.render_template("index.html")

        if sender and subject and email and text:
            contact_form(sender=sender, subject=subject, email=email, text=text)
            params = {"error": "Message successfully sent! :)"}
        else:
            params = {"error": "Please fill all the fields"}

        self.render_template('contact.html', params)


def contact_form(sender, subject, email, text):
    message_body = '''
		New email from ramuta.me!

		Sender: {0}
		Email: {1}
		Subject: {2}
		Text: {3}
	'''.format(sender.encode('utf-8'),
               email.encode('utf-8'),
               subject.encode('utf-8'),
               text.encode('utf-8'))

    html_message_body = '''
		<p>New email from ramuta.me!</p>

		<p>Sender: {0}</p>
		<p>Email: {1}</p>
		<p>Subject: {2}</p>
		<p>Text: {3}</p>
	'''.format(sender.encode('utf-8'),
               email.encode('utf-8'),
               subject.encode('utf-8'),
               text.encode('utf-8'))

    message = mail.EmailMessage(sender="Ramuta.me <matt@ramuta.me>",
                                to="matej.ramuta@gmail.com",
                                subject="Novo sporocilo na ramuta.me",
                                body=message_body,
                                html=html_message_body)
    message.send()


class LoginHandler(Handler):
    def get(self):
        self.redirect(users.create_login_url("/"))


class LogoutHandler(Handler):
    def get(self):
        self.redirect(users.create_logout_url("/"))


"""
class LoginHandler(Handler):
    def get(self):
        User.init()
        self.render('login.html')

    def post(self):
        email = self.request.get("email")
        password = self.request.get("password")
        if email and password:
            user = User.query(User.email == email).get()
            if user:
                if User.check_password(password=password, password_hash=user.password_hash):
                    self.response.headers.add_header('Set-Cookie', 'user_id=%s' % hash_cookie(str(user.key.id())))
                    self.render_template('index.html')
                else:
                    params = {"error": "Password is incorrect"}
                    self.render_template('login.html', params)
            else:
                params = {"error": "User with this email does not exist"}
                self.render_template('login.html', params)
        else:
            params = {"error": "Please fill all the fields"}
            self.render_template('login.html', params)


class LogoutHandler(Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=')
        self.render('login.html')
"""

app = webapp2.WSGIApplication([
                                  webapp2.Route('/', MainHandler, name="main"),
                                  webapp2.Route('/about', AboutHandler, name="about"),
                                  webapp2.Route('/contact', ContactHandler),
                                  webapp2.Route('/login', LoginHandler),
                                  webapp2.Route('/logout', LogoutHandler),
                                  webapp2.Route('/new-post', NewPostHandler),
                                  webapp2.Route('/forbidden', ForbiddenHandler, name="forbidden"),
                              ], debug=True)