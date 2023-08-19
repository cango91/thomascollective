from django.contrib.auth import logout

class PreventDoubleLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/accounts/login/' and request.user.is_authenticated:
            logout(request)
        return self.get_response(request)