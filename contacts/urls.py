# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path('adder/', views.adder, name='adder'),
    path('shower/', views.shower, name='shower'),
    path('searcher/', views.searcher, name='searcher'),
    path('modifier/', views.modifier, name='modifier'),
    path('deleter/', views.deleter, name='deleter'),
    path('modify_contact/', views.modify_contact, name='modify_contact'),
]
