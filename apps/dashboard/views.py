from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.views import LoginView, logout_then_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from apps.core.models import Analyze
from apps.core.forms import UserForm


@method_decorator(login_required, name='dispatch')
class PanelView(TemplateView):
    template_name = 'dashboard/panel.html'
    http_method_names = ['get', 'post']

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        extra_args = []

        if self.request.method == 'POST':
            s = self.request.POST.get('s')
            data['s'] = s.strip()
            extra_args = [
                Q(registration_number__contains=s) |
                Q(address__icontains=s) |
                Q(block__contains=s) |
                Q(zipcode__contains=s) |
                Q(lot__contains=s)
            ]

        data['analyzes'] = Analyze.objects.filter(user=self.request.user, *extra_args)
        return data

    def post(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class AuthView(LoginView):
    template_name = 'dashboard/login.html'
    redirect_authenticated_user = True


class SignupView(FormView):
    template_name = 'dashboard/signup.html'
    form_class = UserForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, 'Bem vindo. Esta é o seu painel, fique a vontade e explore nossa ferramenta.')
        return reverse('dashboard:panel')


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self, request):
        return logout_then_login(request)


@method_decorator(login_required, name='dispatch')
class CreditView(TemplateView):
    template_name = 'dashboard/credit.html'


@method_decorator(login_required, name='dispatch')
class AnalyseFormView(CreateView):
    template_name = 'dashboard/analyze-form.html'
    model = Analyze
    fields = ['zipcode', 'address', 'number', 'registration_number', 'block', 'lot']

    def get_success_url(self):
        return reverse('dashboard:panel')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Solicitação de análise efetuada com sucesso!')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class AnalyseView(TemplateView):
    template_name = 'dashboard/analyze.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        data['analyze'] = Analyze.objects.get(pk=self.request.GET['code'])
        return data