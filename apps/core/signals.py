from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from templated_email import send_templated_mail

from apps.core.models import Analyze, Indicator, Report, Account, User


@receiver(post_save, sender=Analyze)
def create_analyzes_indicators(sender, instance, created, **kwargs):
    if not created:
        return

    with transaction.atomic():
        indicators = Indicator.objects.all()
        bulk = []

        for indicator in indicators:
            bulk.append(Report(analyse=instance, indicator=indicator))

        Report.objects.bulk_create(bulk)


@receiver(post_save, sender=Analyze)
def send_analyzed_email(sender, instance, created, **kwargs):
    if instance.is_analyzed and instance.tracker.has_changed('state'):
        send_templated_mail(
            template_name='analyse-finished',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.user.email],
            context={'analyze': instance}
        )


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account(user=instance).save()
