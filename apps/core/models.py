import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from cities_light.models import Region, City
from model_utils import FieldTracker
from model_utils.models import TimeStampedModel
from extended_choices import Choices
from django.contrib.postgres.fields import JSONField


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    TYPE_CHOICES = (
        ('owner', 'Pessoa Física'),
        ('real_estate', 'Imobiliária')
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0], verbose_name='Qual o seu perfil?')
    whatsapp = models.CharField(max_length=20, verbose_name='WhatsApp', null=True, blank=True)
    document = models.CharField(max_length=20, verbose_name='CPF ou CNPJ', null=True)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=255, null=True, verbose_name=_("Número do seu Endereço"))
    zipcode = models.CharField(max_length=10, null=True, verbose_name=_("CEP do seu Endereço"))
    address = models.CharField(max_length=255, null=True, verbose_name=_("Endereço"))
    district = models.CharField(max_length=255, null=True, verbose_name=_("Bairro"))

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Indicator(BaseModel, TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    observation_ok = models.CharField(max_length=100, verbose_name=_("Ok Observation"), null=True, blank=True)
    observation_not_ok = models.CharField(max_length=100, verbose_name=_("Not Ok Observation"), null=True, blank=True)

    def __str__(self):
        return self.name

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
        ('analyzed', 'analyzed', _("Perished"))
    )
    TYPES = Choices(
        ('apartment', 'apartment', _("Apartment")),
        ('house', 'house', _("House")),
        ('ground', 'ground', _("Ground")),
        ('site', 'site', _("Site"))
    )

    state = models.CharField(max_length=30, choices=STATES, default=STATES.requested, verbose_name=_("State"))
    user = models.ForeignKey('core.User', related_name='analyses', on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=255, null=True, verbose_name=_("Address"))
    number = models.CharField(max_length=255, null=True, verbose_name=_("Number"))
    zipcode = models.CharField(max_length=10, null=True, verbose_name=_("CEP"))
    block = models.CharField(max_length=20, null=True, verbose_name=_("Block"))
    lot = models.CharField(max_length=20, null=True, verbose_name=_("Lot"))
    registration_number = models.CharField(max_length=20, null=True, verbose_name=_("Registration Number"))
    registration = models.FileField(null=True, verbose_name=_("Registration"))
    type = models.CharField(max_length=30, choices=TYPES, default=TYPES.house, verbose_name=_("Type"))
    complement = models.CharField(max_length=100, verbose_name=_("complement"), null=True, blank=True)
    tracker = FieldTracker()

    @property
    def code(self):
        return self.id.hex[:10]

    @property
    def is_analyzed(self):
        return self.state == self.STATES.analyzed

    @property
    def type_display(self):
        _ = self.TYPES.for_constant(self.type)
        return _.display

    @property
    def state_display(self):
        state = self.STATES.for_constant(self.state)
        return state.display

    @property
    def state_badge_class(self):
        if self.state == 'requested':
            return 'badge-info'
        if self.state == 'registration_found':
            return 'badge-warning'
        if self.state == 'analyzed':
            return 'badge-success'

    def __str__(self):
        return self.user.email if self.user else 'N/A'

    class Meta:
        verbose_name = _("Analyse")
        verbose_name_plural = _("Analyses")


class Report(BaseModel, TimeStampedModel):
    STATES = Choices(
        ('ok', 'ok', _("Ok")),
        ('not_ok', 'not_ok', _("Not Ok"))
    )

    analyse = models.ForeignKey(Analyze, verbose_name=_("Analyse"), on_delete=models.CASCADE)
    indicator = models.ForeignKey(Indicator, verbose_name=_("Indicator"), on_delete=models.CASCADE, null=True)
    state = models.CharField(max_length=30, choices=STATES, verbose_name=_("State"), null=True, blank=True  )
    observation = models.CharField(max_length=100, verbose_name=_("Observation"), null=True, blank=True)

    def __str__(self):
        return '{}-{}'.format(self.analyse.address, self.indicator.name)

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")


class Account(BaseModel, TimeStampedModel):
    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE)
    credit = models.DecimalField(max_digits=20, decimal_places=4, verbose_name=_("Credit available for new requests"), default=Decimal('0'))
    credit_used = models.DecimalField(max_digits=20, decimal_places=4, verbose_name=_("Credit used"), default=Decimal('0'))
    request_price = models.DecimalField(max_digits=20, decimal_places=4, verbose_name=_("Request price"), default=Decimal('52.90'))
    requests = models.IntegerField(verbose_name=_("Requests available for free"), default=0)
    iugu_data = JSONField(verbose_name=_("Iugu Credit Card Data"), default=dict)

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")


class Charge(BaseModel, TimeStampedModel):
    STATES = Choices(
        ('created', 'created', _("Criada")),
        ('paid', 'paid', _("Paga"))
    )

    amount = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('0'), verbose_name=_("Valor"))
    user = models.ForeignKey('core.User', related_name='charges', on_delete=models.CASCADE, null=True)
    ref = models.CharField(max_length=300, verbose_name=_("Valor"))
    state = models.CharField(max_length=30, default=STATES.created)

    class Meta:
        verbose_name = _("Cobrança")
        verbose_name_plural = _("Cobranças")
