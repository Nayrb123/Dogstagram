from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^createprofile$', views.createprofile),
    url(r'^registration$', views.processregistration),
    url(r'^login$', views.login),
    url(r'^profilepage/(?P<id>\d+)$', views.profile_page),
    url(r'^editprofile/(?P<id>\d+)$', views.editpage),
    url(r'^processedit/(?P<id>\d+)$', views.processedit),
    url(r'^comment$', views.comment),
]