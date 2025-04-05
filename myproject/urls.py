"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from myapp import views
from django.contrib import admin
urlpatterns = [
    path("admin/",admin.site.urls),
    path('',views.Login,name = 'Login'),
    path('home/',views.home,name = "home"),
    path('logout/',views.Logout,name = "Logout"),
    path('signup/',views.signup,name='signup'),
    path('adminpanel/',views.my_admin,name='myadmin'),
    path('adminpanel/adduser/',views.add_user,name='adduser'),
    path('adminpanel/edituser/<int:user_id>/',views.edit_user,name='edituser'),
    path('adminpanel/delete/<int:user_id>/',views.delete_user,name='deleteuser'),

]
