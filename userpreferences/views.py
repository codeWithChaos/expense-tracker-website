from django.shortcuts import render, redirect
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages


import os
import json
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from .models import UserPreference

def index(request):
    currency_data = []
    # Path to the currencies.json file
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    # Load currencies from the JSON file
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            currency_data.append({'name': key, 'value': value})

    # Check if user preferences exist
    user_preferences = UserPreference.objects.filter(user=request.user).first()

    if request.method == 'POST':
        # Get the selected currency from the form
        currency = request.POST.get('currency')
        
        if user_preferences:
            # Update existing user preference
            user_preferences.currency = currency
            user_preferences.save()
        else:
            # Create a new user preference if none exists
            UserPreference.objects.create(user=request.user, currency=currency)
        
        # Display success message
        messages.success(request, 'Changes saved')
        return redirect('preferences')

        # Update user_preferences after saving the new data
        user_preferences = UserPreference.objects.get(user=request.user)

    # Prepare context for rendering the template
    context = {
        'currencies': currency_data,
        'user_preferences': user_preferences,
    }

    return render(request, 'userpreferences/index.html', context)
