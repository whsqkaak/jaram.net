from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'EXCLUDE_LOGIN_REQUIRED_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.EXCLUDE_LOGIN_REQUIRED_URLS]


class LoginRequiredMiddleware:

    def process_request(self, request):
        assert hasattr(request, 'user'), ""

        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL)
