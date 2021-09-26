from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('add_user/', views.add_user, name='add_user'),
    path('login/', views.login, name='login'),
    path('success/', views.success, name='success'),
    path('log_out/', views.log_out, name='log_out'),
]