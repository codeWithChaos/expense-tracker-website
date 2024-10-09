from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference


@login_required(login_url='/authentication/login')
def index(request):
    catecogories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    # currency = UserPreference.objects.get(user=request.user).currency
    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = 'USD'
    context = {
        'categories': catecogories,
        'expenses': expenses,
        'page_obj': page_obj,
        # 'currency': currency,
    }
    return render(request, 'expenses/index.html', context)

@login_required(login_url='/authentication/login')
def add_expense(request):    
    categories = Category.objects.all()
    today_date = timezone.now().strftime('%Y-%m-%d')
    context = {
        'categories' : categories,
        'value' : request.POST,
        'today_date' : today_date,
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        category = request.POST.get('category')
        date = request.POST.get('expense_date')
        
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)
        
        Expense.objects.create(owner=request.user, amount=amount, description=description, category=category, date=date)
        messages.success(request, 'Expense saved successfully')
        return redirect('home')
        
    return render(request, 'expenses/add_expense.html', context)
        

def edit_expense(request, id):
    # Retrieve the expense object by its ID
    expense = get_object_or_404(Expense, pk=id)
    category = Category.objects.all()
    
    today_date = timezone.now().strftime('%Y-%m-%d')
    context = {
        'expense': expense,
        'values' : expense,
        'categories' : category,
        'today_date' : today_date,
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    
    else:
        if request.method == 'POST':
            amount = request.POST.get('amount')
            description = request.POST.get('description')
            category = request.POST.get('category')
            date = request.POST.get('expense_date')
            
            # Validate the form fields
            if not amount:
                messages.error(request, 'Amount is required')
                return render(request, 'expenses/edit-expense.html', context)
            
            if not description:
                messages.error(request, 'Description is required')
                return render(request, 'expenses/edit-expense.html', context)
            
            # Update the existing expense record
            expense.owner = request.user
            expense.amount = amount
            expense.description = description
            expense.category = category
            expense.date = date
            expense.save()
            
            # expense = Expense.objects.create(owner=request.user, amount=amount, description=description, category=category, date=date)
            messages.success(request, 'Expense updated successfully')
            return redirect('home')
        return render(request, 'expenses/edit-expense.html', context)
    
def delete_expense(request, id):
    expense = get_object_or_404(Expense, pk=id)
    expense.delete()
    messages.success(request, 'Expense deleted successfully')
    return redirect('home')


def search_expenses(request):
    if request.method == 'POST':
        search_string = json.loads(request.body).get('searchText', '')
        
        # Users should only be able to search their own expenses
        expenses = Expense.objects.filter(amount__startswith=search_string, owner=request.user) | Expense.objects.filter(date__icontains=search_string, owner=request.user) | Expense.objects.filter(description__icontains=search_string, owner=request.user) | Expense.objects.filter(category__icontains=search_string, owner=request.user)
        
        data = expenses.values()
        return JsonResponse(list(data), safe=False)