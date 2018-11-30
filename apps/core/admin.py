from django.contrib import admin
from apps.core.models import User, Indicator, Plan, Analyze, Report, Account


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    pass


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    pass


@admin.register(Analyze)
class AnalyzeAdmin(admin.ModelAdmin):
    pass


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass