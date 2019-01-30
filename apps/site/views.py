from django.views.generic import TemplateView
from apps.core.models import Indicator, Report, Analyze


class HomeView(TemplateView):
    template_name = 'site/home.html'


class HowItWorksView(TemplateView):
    template_name = 'site/how-it-works.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['indicators'] = Indicator.objects.all()
        return context


class Step1View(TemplateView):
    template_name = 'site/step-1.html'


class Step2View(TemplateView):
    template_name = 'site/step-2.html'


class Step3View(TemplateView):
    template_name = 'site/step-3.html'


class PlansView(TemplateView):
    template_name = 'site/plans.html'


class ExampleView(TemplateView):
    template_name = 'site/example.html'

    def get_context_data(self, **kwargs):
        analyze = Analyze.objects.filter(state=Analyze.STATES.analyzed).order_by('created').first()
        context = super().get_context_data()
        context['reports'] = Report.objects.filter(analyse=analyze)
        return context
