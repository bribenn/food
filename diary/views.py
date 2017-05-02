from django.shortcuts import render, redirect

# Create your views here.
def current_user(request):
	return User.objects.get(id = request.session['user_id'])

def index(request):
	return render('diary/index.html')

