from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UsernamePasswordResetForm(PasswordChangeForm):
    def get_users(self, username):
        """Override get_users to search by username instead of email"""
        try:
            user = User.objects.get(username=username)
            if user:
                return [user]
        except User.DoesNotExist:
            raise ValidationError("No user found with this username.")