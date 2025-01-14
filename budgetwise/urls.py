from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analytics/', views.analytics, name='analytics'),
    path('updates/', views.updates, name='updates'),
    path('contacts/', views.contacts, name='contacts'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('membership/', views.membership, name='membership'),
    path('change_plan/<str:plan>/', views.change_plan, name='change_plan'),
    path('transactions/add-transaction/', views.add_transaction, name='add_transaction'),
    path('transactions/manage/<int:transaction_id>/', views.transaction_manage, name='transaction_manage'),
]
