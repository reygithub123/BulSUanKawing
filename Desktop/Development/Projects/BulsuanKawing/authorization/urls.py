from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_login),
    path('login/', views.view_login),
    path('signup/', views.view_signup),
]
