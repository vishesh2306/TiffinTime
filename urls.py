"""tiffin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.contrib import admin
from django.urls import path,include,re_path
from . import views 

from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from . import settings

admin.site.site_header="Tiffin Time"
admin.site.colorfield="red"

urlpatterns = [
    re_path(r'^jet/', include('jet.urls', 'jet')),
    re_path(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('',views.Indexpage),
    #path('signup',views.Userreg,name="reg"),
    path('login',views.login,name="log"),
    #path('LOGOUT',views.logout,name="logout"),
    path('home', views.Indexpage),
    path('Menu', views.menu),
    path('about',views.About),
    path('icons',views.icons),
    path('codes',views.codes),
    #path('contact',views.contact),
    path('careers',views.careers),
    path('help',views.pwu),
    path('faq',views.faq),
    path('offers',views.offers),
    path('terms',views.terms),
    path('privacy',views.privacy),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('accounts/', include('accounts.urls')),
    path('accounts/',include('django.contrib.auth.urls')),
    path('', include('pages.urls')),
    #path('contact_us',views.contact_us),
    path('core/', include('core.urls', namespace='core')),

    
   

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
