from django.contrib import admin
from .models import Expense, Category


# Register the models 
admin.site.register(Expense)
admin.site.register(Category)
