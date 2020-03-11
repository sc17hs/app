"""cw1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
from rating import views
from rating.views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^modules/', views.ModuleList.as_view()),
    url(r'^professors/', view, name='view'),
    url(r'^average/(?P<profid>[\w-]+)/(?P<modid>[\w-]+)/$', views.average),
    url(r'register/$',views.CreateUserView.as_view(), name= 'user'),
    #url(r'^auth/', include('rest_auth.urls')),
    url(r'^rating/',views.CreateRatingView.as_view(),name='rating'),
    url(r'^login/',views.LoginView.as_view(), name = 'login'),
]

urlpatterns = format_suffix_patterns(urlpatterns)