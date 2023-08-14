from .utils import generate_token
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


def send_verification_email(user, send_email_func, request=None):
    current_site = get_current_site(request)
    domain = current_site.domain
    token = generate_token(user, domain=domain)
    verification_link = request.build_absolute_uri(reverse('verify_email', args=[token]))

    send_email_func(user, verification_link)
