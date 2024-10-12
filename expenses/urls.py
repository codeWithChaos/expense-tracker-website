from django.urls import path
from .views import index, add_expense, edit_expense, delete_expense, search_expenses, expense_category_summary, stats_view
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', index, name='home'),
    path('add-expense/', add_expense, name='add-expense'),
    path('edit-expense/<int:id>/', edit_expense, name='edit-expense'),
    path('delete-expense/<int:id>/', delete_expense, name='delete-expense'),
    path('search-expenses/', csrf_exempt(search_expenses), name='search-expenses'),
    path('expense-category-summary/', expense_category_summary, name='expense-category-summary'),
    path('stats/', stats_view, name='stats'),
]


