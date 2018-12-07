from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'site/home.html'


class HowItWorksView(TemplateView):
    template_name = 'site/how-it-works.html'


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
