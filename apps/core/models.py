import uuid

from django.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from cities_light.models import Region, City
from model_utils.models import TimeStampedModel
from extended_choices import Choices


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Indicator(BaseModel, TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Indicator")
        verbose_name_plural = _("Indicators")


class Plan(BaseModel, TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    requests_limit = models.IntegerField(verbose_name=_("Requests limit"))
    price = models.DecimalField(max_digits=20, decimal_places=4, verbose_name=_("Price"), null=True)
    region = models.ForeignKey(Region, verbose_name=_("Region"), on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = _("Plan")
        verbose_name_plural = _("Plans")


class Analyze(BaseModel, TimeStampedModel):
    STATES = Choices(
        ('requested', 'requested', _("Requested")),
        ('registration_found', 'registration_found', _("Regisration found")),
        ('analyzed', 'analyzed', _("Analyzed"))
    )

    state = models.CharField(max_length=30, choices=STATES, verbose_name=_("State"))
    region = models.ForeignKey(Region, verbose_name=_("Region"), on_delete=models.CASCADE)
    city = models.ForeignKey(City, verbose_name=_("City"), on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True, verbose_name=_("Address"))
    number = models.CharField(max_length=255, null=True, verbose_name=_("Number"))
    neighborhood = models.CharField(max_length=255, null=True, verbose_name=_("Neighborhood"))
    block = models.CharField(max_length=20, null=True, verbose_name=_("Block"))
    lot = models.CharField(max_length=20, null=True, verbose_name=_("Lot"))
    latitude = PointField(null=True, verbose_name=_("Latitude"))
    longitude = PointField(null=True, verbose_name=_("Longitude"))
    registration = models.FileField(null=True, verbose_name=_("Registration"))

    class Meta:
        verbose_name = _("Analyse")
        verbose_name_plural = _("Analyses")


class Report(BaseModel, TimeStampedModel):
    STATES = Choices(
        ('ok', 'ok', _("Ok")),
        ('not_ok', 'not_ok', _("Not Ok"))
    )

    analyse = models.ForeignKey(Analyze, verbose_name=_("Analyse"), on_delete=models.CASCADE)
    state = models.CharField(max_length=30, choices=STATES, verbose_name=_("State"))

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")


class Account(BaseModel, TimeStampedModel):
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.CASCADE)
    credit = models.DecimalField(max_digits=20, decimal_places=4, verbose_name=_("Credit available for new requests"))
    credit_used = models.DecimalField(max_digits=20, decimal_places=4, verbose_name=_("Credit used"))
    requests = models.IntegerField(verbose_name=_("Requests available for free"))

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")


