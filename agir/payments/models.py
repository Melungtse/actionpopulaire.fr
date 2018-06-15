from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import floatformat
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from agir.lib.models import LocationMixin
from .types import get_payment_choices
from .payment_modes import PAYMENT_MODES


class PaymentQueryset(models.QuerySet):
    def awaiting(self):
        return self.filter(status=Payment.STATUS_WAITING)

    def completed(self):
        return self.filter(status=Payment.STATUS_COMPLETED)

    def failed(self):
        return self.filter(status__in=[Payment.STATUS_ABANDONED, Payment.STATUS_CANCELED, Payment.STATUS_REFUSED])


PaymentManager = models.Manager.from_queryset(PaymentQueryset, class_name='PaymentManager')


class Payment(TimeStampedModel, LocationMixin):
    objects = PaymentManager()

    STATUS_WAITING = 0
    STATUS_COMPLETED = 1
    STATUS_ABANDONED = 2
    STATUS_CANCELED = 3
    STATUS_REFUSED = 4

    STATUS_CHOICES = (
        (STATUS_WAITING, 'En attente'),
        (STATUS_COMPLETED, 'Terminé'),
        (STATUS_ABANDONED, 'Abandonné'),
        (STATUS_CANCELED, 'Annulé'),
        (STATUS_REFUSED, 'Refusé')
    )

    person = models.ForeignKey('people.Person', on_delete=models.SET_NULL, null=True)

    email = models.EmailField('email', max_length=255)
    first_name = models.CharField('prénom', max_length=255)
    last_name = models.CharField('nom de famille', max_length=255)
    phone_number = PhoneNumberField('numéro de téléphone', null=True)

    type = models.CharField("type", choices=get_payment_choices(), max_length=255)
    price = models.IntegerField(_("prix en centimes d'euros"))
    status = models.IntegerField("status", choices=STATUS_CHOICES, default=STATUS_WAITING)
    meta = JSONField(blank=True, default=dict)
    mode = models.CharField(_('Mode de paiement'), max_length=70, null=False, blank=False)
    events = JSONField(_('Événements de paiement'), blank=True, default=list)

    @property
    def price_display(self):
        return "{} €".format(floatformat(self.price / 100, 2))

    def get_payment_url(self):
        return reverse('payment_page', args=[self.pk])
