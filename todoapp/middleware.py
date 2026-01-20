# middleware.py
from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Пытаемся получить TZ из куки
        tzname = request.COOKIES.get('django_timezone')
        if tzname:
            try:
                timezone.activate(tzname)
            except Exception:
                timezone.deactivate()
        else:
            timezone.deactivate()

        return self.get_response(request)
