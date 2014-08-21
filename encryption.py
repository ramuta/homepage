import hmac
from hashlib import sha512
from secret import secret_string

__author__ = 'matej'


def hmac_hash_sha512(key, message):
	return hmac.new(key=key, msg=message, digestmod=sha512).hexdigest()


def hash_cookie(user_id):
	id_hash = hmac_hash_sha512(secret_string, user_id)
	return "%s|%s" % (user_id, id_hash)


def check_cookie_hash(cookie):
	user_id = str(cookie.split("|")[0])
	return hash_cookie(user_id) == str(cookie)