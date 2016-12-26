from django.conf.urls import patterns, url
from login_old import views

urlpatterns = patterns('',
                       url(r'^login/$', views.login, name='login'),
                       url(r'^create/$', views.create, name='create'),
                       )