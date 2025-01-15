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
    path('transactions/', views.all_transactions, name='all_transactions'),
    path('goals/add-saving_goal/', views.add_saving_goal, name='add_saving_goal'),
    path('goals/manage/<int:saving_goal_id>/', views.saving_goal_manage, name='saving_goal_manage'),
    path('budgets/add-budget/', views.add_budget, name='add_budget'),
    path('budgets/manage/<int:budget_id>/', views.budget_manage, name='budget_manage'),
    path('notifications/mark_all_as_read/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
]
