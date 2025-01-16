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
    path('transactions/', views.TransactionListView.as_view(), name='all_transactions'),
    path('transactions/add/', views.TransactionCreateView.as_view(), name='add_transaction'),
    path('goals/add/', views.SavingGoalCreateView.as_view(), name='add_saving_goal'),
    path('budgets/add/', views.BudgetCreateView.as_view(), name='add_budget'),
    path('budgets/edit/<int:budget_id>/', views.budget_manage, name='budget_manage'),
    path('goals/edit/<int:saving_goal_id>/', views.saving_goal_manage, name='saving_goal_manage'),
    path('transactions/edit/<int:transaction_id>/', views.transaction_manage, name='transaction_manage'),
    path('notifications/read/', views.mark_all_notifications_as_read, name='mark_all_notifications_as_read'),
]