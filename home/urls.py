from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('login',views.signin,name='login'),
    path('logout', views.logout, name='logout'),
    path("forgot-password", views.forgot_password, name="forgot_password"),
    path("reset-password", views.reset_password, name="reset_password"),
    path('dashboard',views.dashboard,name='dashboard'),
    path('add-category',views.add_category,name='add_category'),
    path('edit-category', views.edit_category, name='edit_category'),
    path('delete-category/<int:id>', views.delete_category, name='delete_category'),
    path('categories', views.category_list, name='category_list'),
    path('add-expense', views.add_expense, name='add_expense'),
    path('expenses', views.expenses_list, name='expenses_list'),
    path('edit-expense/<int:id>', views.edit_expense, name='edit_expense'),
    path('delete-expense/<int:id>', views.delete_expense, name='delete_expense'),
    path('budget', views.budget_view, name='budget'),
    path('add-income', views.add_income, name='add_income'),
    path('income', views.income_list, name='income_list'),
    path('edit-income/<int:id>', views.edit_income, name='edit_income'),
    path('delete-income/<int:id>', views.delete_income, name='delete_income'),
    path('expense-report', views.expense_report, name='expense_report'),
    path('monthly-report',views.monthly_expense_report,name='monthly_expense_report'),
]
