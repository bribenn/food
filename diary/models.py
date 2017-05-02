from __future__ import unicode_literals

from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
	def validateUser(self, post_data):

		is_valid = True
		errors = []

		if len(post_data.get('username')) < 3:
			is_valid = False
			errors.append('username must be more than 3 characters')
		#if email is valid
		if not re.search(r'\w+\@\w+.\w+', post_data.get('email')):
			is_valid = False
			errors.append('must enter a valid email')
		#if password >= 8 characters, matches password confirmation
		if len(post_data.get('password')) < 8:
			is_valid = False
			errors.append('password must be at least 8 characters')
		if post_data.get('password_confirmation') != post_data.get('password'):
			is_valid = False
			errors.append('password and password confirmation must match')

		return (is_valid, errors)


class User(models.Model):
	username = models.CharField(max_length = 45)
	email = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class User_profileManager(Models.Manager):
	pass

class User_profile(models.Model):
	user = models.ForeignKey(User, related_name = 'profile')
	birthdate = models.DateField()
	height = models.DecimalField(max_digits=5, decimal_places=2)
	weight = models.DecimalField(max_digits=5, decimal_places=2)
	diet = models.CharField(max_length = 45)
	calories_per_day = models.IntegerField()
	gender = models.CharField(max_length = 6)
	goal = models.TextField()
	activity_level = TextField()
	objects = User_profileManager()


	
		

