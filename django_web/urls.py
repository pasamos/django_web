"""django_web URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from ccblog import views as ccblog_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', ccblog_views.login),
    url(r'^login/', ccblog_views.login),
    url(r'^logout/', ccblog_views.logout),
    url(r'^blogtype/',ccblog_views.user_blogtype),
    url(r'^addblogtype/',ccblog_views.user_addblogtype),
    url(r'^delblogtype/',ccblog_views.user_delblogtype),
    url(r'^editblogtype/',ccblog_views.user_editblogtype),
    url(r'^blog/',ccblog_views.user_blog),
]
