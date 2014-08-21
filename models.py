from google.appengine.ext import ndb
from encryption import hmac_hash_sha512
from secret import secret_string

__author__ = 'matej'


class User(ndb.Model):
	first_name = ndb.StringProperty()
	last_name = ndb.StringProperty()
	email = ndb.StringProperty()
	password_hash = ndb.StringProperty(default="123456dsfds")

	@classmethod
	def check_password(cls, password, password_hash):
		pw_hash = hmac_hash_sha512(secret_string, password)
		return password_hash == pw_hash

	@classmethod
	def create(cls, first_name, last_name, email):
		user = cls(first_name=first_name, last_name=last_name, email=email)
		user.put()

	@classmethod
	def init(cls):
		user = User.query(User.email == "matej.ramuta@gmail.com").get()
		if not user:
			User.create(first_name="Matej", last_name="Ramuta", email="matej.ramuta@gmail.com")


class BlogPost(ndb.Model):
	title = ndb.StringProperty()
	slug = ndb.StringProperty(default="none")
	text = ndb.TextProperty()
	author = ndb.StringProperty()
	datetime = ndb.DateTimeProperty(auto_now_add=True)

	@property
	def get_id(self):
		return self.key().id

	@classmethod
	def create(cls, title, text):
		post = cls(title=title,
		           text=text,
		           author="Matt Ramuta")
		post.put()