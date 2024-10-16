from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from .forms import UsernamePasswordResetForm
from django.urls import reverse_lazy


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        # Get user data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        context = {
            'fieldValues': request.POST,
        }
        
        # validate
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html')

                # create a user account
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                # user.is_active = False
                user.save()
                # email_subject = 'Activate your account'
                # email_body = 'Test body'
                # email = EmailMessage(
                #     email_subject,
                #     email_body,
                #     'noreply@blackchaos.com',
                #     [email],
                # )
                
                # email.send(fail_silently=False)
                messages.success(request, 'Account created successfully')
                return render(request, 'authentication/register.html')
        return render(request, 'authentication/register.html')
    

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=409)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'username already taken. Select another one.'}, status=400)
        return JsonResponse({'username_valid': True})
    
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        
        if not validate_email(email):
            return JsonResponse({'email_error': 'email is invalid'}, status=409)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'email already taken. Select another one.'}, status=400)
        return JsonResponse({'email_valid': True})
    
    
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = auth.authenticate(username=username, password=password)
            
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f"Welcome,  {user.username}! You're now logged in.")
                    return redirect('home')
                messages.error(request, 'Account not active, please contact admin!')
                return render(request, 'authentication/login.html')
            messages.error(request, 'Invalid credentials, try again!')
            return render(request, 'authentication/login.html')
        messages.error(request, 'Please fill all fields!')
        return render(request, 'authentication/login.html')
            
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out!')
        return redirect('login')
    
    
class ResetPasswordView(PasswordResetView):
    form_class = UsernamePasswordResetForm
    template_name = 'authentication/password_reset.html'
    success_url = reverse_lazy('password_reset_done') 
    


