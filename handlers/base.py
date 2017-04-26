import webapp2
import os
import jinja2
from google.appengine.api import users

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
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
            if users.is_current_user_admin():
                params["hello"] = "Hello, Matej"
                params["admin"] = True
        t = jinja_env.get_template(view_filename)
        self.write(t.render(params))
