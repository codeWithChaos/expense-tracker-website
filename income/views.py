from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Income, Source
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
import json
from django.http import JsonResponse
from django.db.models import Q


@login_required(login_url='/authentication/login')
def index(request):
    sources = Source.objects.all()
    income = Income.objects.filter(owner=request.user)
    paginator = Paginator(income, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    # currency = UserPreference.objects.get(user=request.user).currency
    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = 'USD'
    context = {
        'sources': sources,
        'income': income,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'income/index.html', context)

@login_required(login_url='/authentication/login')
def add_income(request):    
    sources = Source.objects.all()
    today_date = timezone.now().strftime('%Y-%m-%d')
    context = {
        'sources' : sources,
        'value' : request.POST,
        'today_date' : today_date,
    }
    if request.method == 'GET':
        return render(request, 'income/add-income.html', context)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        source = request.POST.get('source')
        date = request.POST.get('income_date')
        
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add-income.html', context)
        
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add-income.html', context)
        
        Income.objects.create(owner=request.user, amount=amount, description=description, source=source, date=date)
        messages.success(request, 'Record saved successfully')
        return redirect('income')
        
    return render(request, 'income/add-income.html', context)
        
@login_required(login_url='/authentication/login')
def edit_income(request, id):
    income = get_object_or_404(Income, pk=id)
    sources = Source.objects.all()
    
    
    if request.method == 'GET':
        # Prefill the form with the existing data
        context = {
            'income': income,
            'values': {
                'amount': income.amount,
                'description': income.description,
                'source': income.source,
                'date': income.date.strftime('%Y-%m-%d'),
            },
            'sources': sources,
        }
        return render(request, 'income/edit-income.html', context)
    else:
        if request.method == 'POST':
            amount = request.POST.get('amount')
            description = request.POST.get('description')
            source = request.POST.get('source')
            date = request.POST.get('income_date')
            
            context = {
                'income': income,
                'values': request.POST,
                'sources': sources,
            }
            
            # Validate the form data
            if not amount:
                messages.error(request, 'Amount is required')
                return render(request, 'income/edit-income.html', context)
            
            if not description:
                messages.error(request, 'Description is required')
                return render(request, 'income/edit-income.html', context)
            
            # Update the existing Income object with the new data
            income.owner = request.user
            income.amount = amount
            income.description = description
            income.source = source
            income.date = date
            income.save()
            
            messages.success(request, 'Income updated successfullu')
            return redirect('income')
        
        return render(request, 'income/edit-income.html', context)

def delete_income(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income deleted successfully')
    return redirect('income')
        
    
def search_income(request):
    if request.method == 'POST':
        search_data = json.loads(request.body)
        search_text = search_data.get('searchText', '')
        
        income = Income.objects.filter(
            Q(amount__istartswith=search_text) |
            Q(source__icontains=search_text)|
            Q(description__icontains=search_text)|
            Q(date__icontains=search_text),
            owner=request.user
        )
        
        data = income.values('amount', 'source', 'description', 'date')
        return JsonResponse(list(data), safe=False)