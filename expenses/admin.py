from django.contrib import admin
from .models import Expense, Category


class AdminExpense(admin.ModelAdmin):
    list_display = ('amount', 'description', 'category', 'date', 'owner')
    search_fields = ['description', 'category', 'date', 'owner__username']
    
    list_per_page = 5
    

admin.site.register(Expense, AdminExpense)
admin.site.register(Category)
