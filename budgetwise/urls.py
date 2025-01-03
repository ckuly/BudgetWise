from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analytics/', views.analytics, name='analytics'),
    path('updates/', views.updates, name='updates'),
    path('newsletter/', views.newsletter, name='newsletter'),
    path('contacts/', views.contacts, name='contacts'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    # path('profile/', views.profile, name='profile'),
]
