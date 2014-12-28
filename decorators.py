from google.appengine.api import users
from webapp2 import redirect, redirect_to
from secret import emails


def login_required(handler):
    def check_login(self, *args, **kwargs):
        user = users.get_current_user()
        if user:
            email = user.email()
            if email in emails:
                return handler(self, *args, **kwargs)
            else:
                return redirect_to("forbidden")
        else:
            return redirect(users.create_login_url("/"))
    return check_login