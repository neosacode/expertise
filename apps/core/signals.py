from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from templated_email import send_templated_mail

from apps.core.models import Analyze, Indicator, Report


# Insert indicators for analyze
@receiver(post_save, sender=Analyze)
def create_user_profile(sender, instance, created, **kwargs):
    if instance.is_analyzed and instance.tracker.has_changed('state'):
        send_templated_mail(
            template_name='analyse-finished',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.user.email],
            context={'analyze': instance}
        )

    if not created:
        return

    with transaction.atomic():
        indicators = Indicator.objects.all()
        bulk = []

        for indicator in indicators:
            bulk.append(Report(analyse=instance, indicator=indicator))

        Report.objects.bulk_create(bulk)
