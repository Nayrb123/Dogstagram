from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^createprofile$', views.createprofile),
    url(r'^registration$', views.processregistration),
    url(r'^login$', views.login),
    url(r'^profilepage$', views.profile_page),
]