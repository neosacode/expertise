from django.views.generic import TemplateView, View
from django.contrib.auth.views import LoginView, logout_then_login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class PanelView(TemplateView):
    template_name = 'dashboard/panel.html'


class AuthView(LoginView):
    template_name = 'dashboard/login.html'
    redirect_authenticated_user = True


class LogoutView(View):
    def get(self, request):
        return logout_then_login(request)
