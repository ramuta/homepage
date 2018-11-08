import json
import logging
import os

from handlers.base import Handler
import urllib
from google.appengine.api import mail
from google.appengine.api import urlfetch

from secrets import get_recaptcha_secret


class ContactHandler(Handler):
    def get(self):
        self.render_template('contact.html')

    def post(self):
        sender = self.request.get("sender")
        subject = self.request.get("subject")
        email = self.request.get("email")
        text = self.request.get("text")
        hidden = self.request.get("skrito")

        # check reCaptcha token
        recaptcha = False
        try:
            form_data = urllib.urlencode({"response": hidden, "secret": get_recaptcha_secret()})
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            result = urlfetch.fetch(
                url='https://www.google.com/recaptcha/api/siteverify',
                payload=form_data,
                method=urlfetch.POST,
                headers=headers)

            result_dict = json.loads(result.content)

            if result_dict["success"]:
                recaptcha = True

        except urlfetch.Error:
            logging.exception('Caught exception fetching url')

        if recaptcha:
            if sender and subject and email and text:
                contact_form(sender=sender, subject=subject, email=email, text=text)
                params = {"error": "Message successfully sent! :)"}
            else:
                params = {"error": "Please fill all the fields"}
        else:
            params = {"error": "Sorry, but it seems you're a robot!"}

        return self.render_template('contact.html', params)


def is_local():
    if os.environ.get('SERVER_NAME', '').startswith('localhost'):
        return True
    elif 'development' in os.environ.get('SERVER_SOFTWARE', '').lower():
        return True
    else:
        return False


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

    if not is_local():
        message = mail.EmailMessage(sender="Ramuta.me <matt@ramuta.me>",
                                    to="matej.ramuta@gmail.com",
                                    subject="Novo sporocilo na ramuta.me",
                                    body=message_body,
                                    html=html_message_body)
        message.send()
