"""weitac_gateway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls import url
from django.contrib import admin
from services.views import ServiceViewSet
from login.views import login, create
urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'weitac_gateway.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^login/', login),
                       url(r'^create/', create),

                       url(r'^admin/', admin.site.urls),
                       url(r'^services/?',
                           ServiceViewSet.as_view({'post': 'create_services',
                                                   'put': 'update_services',
                                                   'delete': 'delete_services',
                                                   'get': 'get_services',
                                                   })),

                       url(r'^continer/?',
                           ServiceViewSet.as_view({'post': 'create_continer'
                                                   # 'put': 'update_services',
                                                   # 'get': 'get_services',
                                                   # 'delete': 'delete_services'
                                                   })),
                       )
