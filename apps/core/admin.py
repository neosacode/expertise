from django.contrib import admin
from apps.core.models import User, Indicator, Plan, Analyze, Report, Account


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    pass


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    pass


class ReportInline(admin.TabularInline):
    model = Report
    readonly_fields = ('indicator',)
    fields = ('indicator', 'state', 'observation',)

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj):
        return False


@admin.register(Analyze)
class AnalyzeAdmin(admin.ModelAdmin):
    list_display = ['get_user', 'zipcode', 'address', 'number', 'registration_number', 'block', 'lot', 'state']
    readonly_fields = ['user', 'address', 'number', 'zipcode', 'block', 'lot', 'registration_number']
    list_filter = ['state']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    inlines = [
        ReportInline
    ]

    def get_user(self, o):
        return o.user.first_name + ' ' + o.user.last_name if o.user else None
    get_user.short_description = 'Usuário'
    get_user.admin_order_field = 'user__username'


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'user__username', 'user__document', 'user__whatsapp']
    list_display = ['user', 'credit', 'credit_used', 'request_price']
