from django.contrib.auth.mixins import LoginRequiredMixin


class LoginRequired(LoginRequiredMixin):
    login_url = '/login/'
