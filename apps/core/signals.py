from django.contrib.auth.models import User
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.core.models import Analyze, Indicator, Report


# Insert indicators for analyze
@receiver(post_save, sender=Analyze)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    with transaction.atomic():
        indicators = Indicator.objects.all()
        bulk = []

        for indicator in indicators:
            bulk.append(Report(analyse=instance, indicator=indicator))

        Report.objects.bulk_create(bulk)
