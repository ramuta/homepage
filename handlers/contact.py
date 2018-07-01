from handlers.base import Handler
from google.appengine.api import mail


class ContactHandler(Handler):
    def get(self):
        self.render_template('contact.html')

    def post(self):
        sender = self.request.get("sender")
        subject = self.request.get("subject")
        email = self.request.get("email")
        text = self.request.get("text")
        hidden = self.request.get("skrito")

        if hidden or "loan" in sender.lower() or "loan" in text.lower():
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
