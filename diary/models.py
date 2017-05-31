from __future__ import unicode_literals

from django.db import models
import re

# Create your models here.
class Food(models.Model):
	name = models.CharField(max_length = 255)
	meal = models.CharField(max_length = 10)
	calories = models.IntegerField()
	carbs = models.IntegerField()
	protein = models.IntegerField()
	fat = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	def __str__(self):
		return	"name:{}, meal:{}, calories:{}, carbs:{}, protein:{}, fat:{}, created_at:{}, updated_at:{}".format(self.name, self.meal, self.calories, self.carbs, self.protein, self.fat, self.created_at, self.updated_at)

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
	food = models.ManyToManyField(Food, related_name = 'user_food')
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class UserProfileManager(models.Manager):
	def validateUserProfile(self, post_data):

		is_valid = True
		errors = []

		if len(post_data.get('birthdate')) == 0:
			is_valid = False
			errors.append('Please enter your birthdate')
		if len(post_data.get('height')) == 0:
			is_valid = False
			errors.append('Please enter your height')
		if len(post_data.get('weight')) == 0:
			is_valid = False
			errors.append('Please enter your weight')
		if len(post_data.get('diet')) == 0:
			is_valid = False
			errors.append('Please enter your dietary preference')
		if len(post_data.get('calories_per_day')) == 0:
			is_valid = False
			errors.append('Please enter your desired calories per day')
		if len(post_data.get('gender')) == 0:
			is_valid = False
			errors.append('Please choose a gender')
		if len(post_data.get('goal')) == 0:
			is_valid = False
			errors.append('Please enter your goal')
		if len(post_data.get('activity_level')) == 0:
			is_valid = False
			errors.append('Please enter your activity level')

		return (is_valid, errors)

class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name = 'profile')
	birthdate = models.DateField()
	height = models.DecimalField(max_digits=5, decimal_places=2)
	weight = models.DecimalField(max_digits=5, decimal_places=2)
	photo = models.ImageField(upload_to=None, max_length=100, default=None)
	diet = models.CharField(max_length = 45)
	calories_per_day = models.IntegerField()
	gender = models.CharField(max_length = 6)
	goal = models.TextField()
	activity_level = models.TextField()
	objects = UserProfileManager()



	
		

