from google.appengine.api import users
from handlers.base import Handler


class LoginHandler(Handler):
    def get(self):
        self.redirect(users.create_login_url("/"))


class LogoutHandler(Handler):
    def get(self):
        self.redirect(users.create_logout_url("/"))
