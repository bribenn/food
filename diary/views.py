from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import datetime
import bcrypt

# Create your views here.
def current_user(request):
	return User.objects.get(id = request.session['user_id'])

def index(request):
	return render(request, 'diary/index.html')

def register(request):
	check = User.objects.validateUser(request.POST)
	if request.method != 'POST':
		return redirect('/')
	if check[0] == False:
		for error in check[1]:
			messages.add_message(request, messages.INFO, error, extra_tags="registration")
			return redirect('/')
	if check[0] == True:
		#has password
		hashed_pw = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt())

		#create user
		user = User.objects.create(
			username = request.POST.get('username'),
			email = request.POST.get('email'),	
			password = hashed_pw,
		)


		#add user to session, logging them in
		request.session['user_id'] = user.id
		#route to profile form page
		return redirect('/profile_form')

def login(request):
	if request.method != 'POST':
		return redirect('/')
	#find user
	user = User.objects.filter(email = request.POST.get('email')).first()

	#Check user credentials
	#add them to session and log in or add error message and route to user profile page
	if user and bcrypt.checkpw(request.POST.get('password').encode(), user.password.encode()):
		request.session['user_id'] = user.id
		return redirect('/user_profile')
	else: 
		messages.add_message(request, messages.INFO, 'invalid credentials', extra_tags="login")
		
	return redirect('/')

def logout(request):
	request.session.clear()
	return redirect('/')

def profile_form(request):
	return render(request, 'diary/profile_form.html')



def add_profile(request):
	check = UserProfile.objects.validateUserProfile(request.POST)
	if request.method != 'POST':
		return redirect('/profile_form')
	if check[0] == False:
		for error in check[1]:
			messages.add_message(request, messages.INFO, error, extra_tags="profile_form")
			return redirect('/profile_form')
	if check[0] == True:
		user = current_user(request)

		profile = UserProfile.objects.create(
				user = user,
				birthdate = request.POST.get('birthdate'),
				height = request.POST.get('height'),
				weight = request.POST.get('weight'),
				diet = request.POST.get('diet'),
				calories_per_day = request.POST.get('calories_per_day'),
				gender = request.POST.get('gender'),
				goal = request.POST.get('goal'),
				activity_level = request.POST.get('activity_level'),
			)

		return redirect('/user_profile')

def show_user_profile(request):
	if 'user_id' in request.session:
		user = current_user(request)
		user_profile = UserProfile.objects.filter(user = user).first()
		user_profile.birthdate = user_profile.birthdate.strftime('%Y-%m-%d')
		today = datetime.datetime.now().strftime('%Y-%m-%d')
		today_food = Food.objects.filter(created_at__startswith=today)
		calories_goal = user_profile.calories_per_day
		today_calories = sum(today_food.values_list('calories', flat=True))
		protein_goal = int((calories_goal * .3) / 4)
		today_protein = sum(today_food.values_list('protein', flat=True))
		carbs_goal = int((calories_goal * .5)/4)
		today_carbs = sum(today_food.values_list('carbs', flat=True))
		fat_goal = int((calories_goal * .2)/7) 
		today_fat = sum(today_food.values_list('fat', flat=True))
		today_breakfast = today_food.filter(name = "breakfast")
		today_lunch = today_food.filter(name = "lunch")
		today_dinner = today_food.filter(name = "dinner")
		today_snack = today_food.filter(name = "snack")
		context = {
		# calories and macros
			'today': today,
			'user': user,
			'user_profile': user_profile,
			'calories_left': calories_goal - today_calories,
			'protein_left': protein_goal - today_protein,
			'carbs_left': carbs_goal - today_carbs,
			'fat_left': fat_goal - today_fat,
			'calories_eaten': today_calories,
		# showing food entered for the day
			'today_food': today_food
		}
		return render(request, 'diary/user_profile.html', context)

	return redirect('/')

def add_food(request):
	user = current_user(request)

	food = Food.objects.create(
			name = request.POST.get('name'),
			meal = request.POST.get('meal'),
			calories = request.POST.get('calories'),
			carbs = request.POST.get('carbs'),
			protein = request.POST.get('protein'),
			fat = request.POST.get('fat'),
		)
	food.user_food.add(user)

	return redirect('/user_profile')

def add_symptoms(request):
	pass

def diary(request):
	pass

def update_profile(request):
	user = current_user(request)

	profile = UserProfile.objects.get(user = user)
			
	profile.birthdate = request.POST.get('birthdate')
	profile.height = request.POST.get('height')
	profile.weight = request.POST.get('weight')
	profile.photo = request.POST.get('photo')
	profile.diet = request.POST.get('diet')
	profile.calories_per_day = request.POST.get('calories_per_day')
	profile.gender = request.POST.get('gender')
	profile.goal = request.POST.get('goal')
	profile.activity_level = request.POST.get('activity_level')

	profile.save()

	return redirect('/user_profile')



