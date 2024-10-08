from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category, Expense


@login_required(login_url='/authentication/login')
def index(request):
    catecogories = Category.objects.all()
    context = {
        'categories': catecogories
    }
    return render(request, 'expenses/index.html', context)

@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories
    }
    return render(request, 'expenses/add_expense.html', context)
