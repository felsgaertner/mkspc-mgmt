from django.conf import settings


def custom_context(request):
    return {
        'BUILD_DATE': settings.BUILD_DATE,
    }
