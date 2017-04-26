from google.appengine.api import users
from webapp2 import redirect, redirect_to


def login_required(handler):
    def check_login(self, *args, **kwargs):
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                return handler(self, *args, **kwargs)
            else:
                return redirect_to("forbidden")
        else:
            return redirect(users.create_login_url("/"))
    return check_login
