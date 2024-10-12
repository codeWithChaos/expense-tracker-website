from django.urls import path
from .views import RegistrationView, UsernameValidationView, EmailValidationView, LoginView, LogoutView, PasswordResetView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', RegistrationView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('validate-username', UsernameValidationView.as_view(), name='validate-username'),
    path('validate-email', EmailValidationView.as_view(), name='validate-email'),
    path('reset-password', PasswordResetView.as_view(), name='password_reset'),
]
