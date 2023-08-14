from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .utils import verify_token
from .exceptions import TokenExpired, InvalidDomain
from .email_utils import send_verification_email

def verify_email_view(request, token):
    try:
        result = verify_token(token)
        if result:
            success_url = getattr(settings, 'EMAIL_VERIFY_SUCCESS_URL', reverse('email_verify:email_verification_success'))
            return redirect(success_url)
        else:
            failure_url = getattr(settings, 'EMAIL_VERIFY_FAILURE_URL', reverse('email_verify:email_verification_failed'))
            return HttpResponseRedirect(failure_url)
    except TokenExpired as e:
        # Optionally resend token if enabled in settings
        if getattr(settings, 'EMAIL_VERIFY_RESEND_ON_EXPIRE', False):
            send_verification_email(request.user, send_email_func=settings.EMAIL_VERIFY_SEND_FUNC, request=request)
        context = {'error':  {'message': str(e), 'error': e}, 'user': request.user}
        # Allow custom template override
        template_name = getattr(settings, 'EMAIL_VERIFY_ERROR_TEMPLATE', 'email_verify/verification_error')
        return render(request, template_name, context)
    except InvalidDomain as e:
        context = {'error':  {'message': str(e), 'error': e}, 'user': request.user}
        # Allow custom template override
        template_name = getattr(settings, 'EMAIL_VERIFY_ERROR_TEMPLATE', 'email_verify/verification_error')
        return render(request, template_name, context)

def verification_failed(request):
    return render(request, 'email_verify/verification_error', {
        'user': request.user
    })

def verification_success(request):
    return render(request, 'email_verify/verification_success', {
        'user': request.user
    })
    
def resend_verification_email_view(request):
    # Optionally check user authentication or other conditions
    user = request.user
    send_verification_email(user, send_email_func=settings.EMAIL_VERIFY_SEND_FUNC, request=request)
    return redirect(reverse('email_verify:email_verification_resend_success'))

def email_verification_resend_success(request):
    return render(request, 'email_verify/verification_resend_success.html', {'user': request.user})

def email_verification_sent(request):
    return render(request, 'email_verify/verification_sent.html', {'user': request.user})