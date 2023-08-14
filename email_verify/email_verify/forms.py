from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse
from .email_utils import send_verification_email

class UserCreationForm(UserCreationForm):
    def save(self, commit=True, request=None):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Send the verification email
            send_verification_email(user, send_email_func=settings.EMAIL_VERIFY_SEND_FUNC, request=request)
            # Redirect to the verification sent page
            return redirect(reverse('email_verify:email_verification_sent'))
        return user