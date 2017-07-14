from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^profile_form$', views.profile_form),
    url(r'^add_profile$', views.add_profile),
    url(r'^user_profile', views.show_user_profile),
    url(r'^add_food', views.add_food),
    url(r'^add_symptoms', views.add_symptoms),
    url(r'^diary', views.diary),
    url(r'^update_profile', views.update_profile),
    url(r'^add_food', views.add_meal)
]