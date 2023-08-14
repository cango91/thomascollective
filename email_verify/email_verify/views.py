from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .utils import verify_token
from .exceptions import TokenExpired, InvalidDomain

def verify_email_view(request, token):
    try:
        result = verify_token(token)
        if result:
            success_url = getattr(settings, 'EMAIL_VERIFY_SUCCESS_URL', '/verification_success/')
            return HttpResponseRedirect(success_url)
        else:
            failure_url = getattr(settings, 'EMAIL_VERIFY_FAILURE_URL', '/verification_failed/')
            return HttpResponseRedirect(failure_url)
    except (TokenExpired, InvalidDomain) as e:
        context = {'error': str(e)}
        return render(request, 'email_verify/verification_error.html', context)