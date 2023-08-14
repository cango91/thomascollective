from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from django.conf import settings
from .models import EmailVerification
from .exceptions import *


def generate_token(user, domain=None):
    if domain is None and not settings.DEBUG:
        raise ValueError("Domain must be provided in production environment.")
    expires = getattr(settings,'EMAIL_VERIFY_EXPIRES_IN',3600)
    s = Serializer(settings.SECRET_KEY, expires_in=expires)
    return s.dumps({'user_id': user.id, 'domain': domain}).decode('utf-8')


def verify_token(token):
    s = Serializer(settings.SECRET_KEY)
    try:
        data = s.loads(token)
    except SignatureExpired:
        raise TokenExpired("Token has expired.")
    except:
        return None

    domain = data.get('domain')
    user_id = data.get('user_id')
    if not settings.DEBUG and domain not in settings.ALLOWED_HOSTS:
        raise InvalidDomain("Invalid domain.")
    if user_id:
        try:
            email_verification = EmailVerification.objects.get(user__id=user_id)
            email_verification.is_verified = True
            email_verification.save()
            return True
        except EmailVerification.DoesNotExist:
            return None
    return None