from decimal import Decimal
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.views import LoginView, logout_then_login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from templated_email import send_templated_mail
from django.db import transaction
from pagseguro import PagSeguro
from apps.core.models import Analyze, Report, Account, User
from apps.core.forms import UserForm
from apps.dashboard.forms import AnalyseForm


pg = PagSeguro(email="esabadini@yahoo.com", token="31E3149BE6E246428498561D5D261021")


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
        user = form.save(commit=False)
        user.username = user.email
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)

        if user.type == 'owner':
            return redirect(self.get_success_url())

        return redirect(reverse('dashboard:wait'))

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['account'] = Account.objects.filter(user=self.request.user).first()
        return context


@method_decorator(login_required, name='dispatch')
class WaitView(TemplateView):
    template_name = 'dashboard/wait.html'


@method_decorator(login_required, name='dispatch')
class AnalyseFormView(CreateView):
    template_name = 'dashboard/analyze-form.html'
    model = Analyze
    form_class = AnalyseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['account'] = Account.objects.filter(user=self.request.user).first()
        return context

    def get_success_url(self):
        return reverse('dashboard:panel')

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.user = self.request.user
            messages.success(self.request, 'Solicitação de análise efetuada com sucesso!')
            response = super().form_valid(form)

            account = Account.objects.filter(user=self.request.user).first()
            account.credit -= account.request_price
            account.save()

        send_templated_mail(
            template_name='new-analyse',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.request.user.email],
            context={'analyze': form.instance}
        )

        return response


@method_decorator(login_required, name='dispatch')
class AnalyseView(TemplateView):
    template_name = 'dashboard/analyze.html'

    def get_context_data(self, **kwargs):
        analyse = Analyze.objects.get(pk=self.request.GET['code'], user=self.request.user)

        data = super().get_context_data()
        data['analyze'] = analyse
        data['reports'] = Report.objects.filter(analyse=analyse)
        return data


@method_decorator(login_required, name='dispatch')
class CreatePaymentView(View):
    def post(self, request):
        amount = round(Decimal(''.join(c for c in request.POST['amount'] if c.isdigit() or c == '.')), 2)

        if amount < 52.90:
            return

        pg.sender = {
            "name": request.user.first_name,
            "email": request.user.email,
        }

        pg.items = []
        pg.add_item(id="0001", description="Crédito conta Imóvel Periciado", amount=str(amount), quantity=1)
        pg.shipping = {
            "type": pg.NONE,
            "street": "AV Beira Mar 5",
            "number": 2560,
            "complement": "",
            "district": "Pontal",
            "postal_code": "89249000",
            "city": "Itapoa",
            "state": "PR",
            "country": "BRA"
        }
        pg.reference_prefix = None
        pg.reference = str(request.user.pk)

        response = pg.checkout()
        return JsonResponse({'code': response.code})


@method_decorator(csrf_exempt, name='dispatch')
class PagseguroNotification(View):
    STATUS_PAGO = 3

    def post(self):
        notification_code = request.POST['notificationCode']
        notification_data = pg.check_notification(notification_code)

        if notification_data['status'] == self.STATUS_PAGO:
            user = User.objects.get(pk=notification_data['reference'])
            account = Account.objects.get(user=user)
            account.credit += Decimal(notification_data['grossAmount'])
            return JsonResponse({'status': 'Payment processed!'})

        return JsonResponse({'status': 'Nothing done!'})

