from django.db import models
import uuid

# Create your models here.

class Guest(models.Model):

    passport = 'PASSPORT'
    idcard = 'IDCARD'
    driverlicense = 'DRIVERLICENSE'
    identy_choices = (
        (passport, 'PASSPORT'),
        (idcard, 'ID CARD'),
        (driverlicense, "DRIVER'S LICENSE"),
    )

    creditcard = 'Creditcard'
    cheque = 'Cheque'
    cash = 'Cash'
    payment_choices = (
        (creditcard, 'Creditcard'),
        (cheque, 'Cheque'),
        (cash, "Cash"),
    )

    id = models.UUIDField(primary_key=True, editable=False, default = uuid.uuid4)
    fullname = models.CharField(max_length=100, blank=False)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    middle_name = models.CharField(max_length=100, blank=True)
    official_title = models.CharField(max_length=100, blank=True)
    identification = models.CharField(default=passport, choices=identy_choices, max_length=50, blank=False)
    payment_type = models.CharField(default=creditcard, choices=payment_choices, max_length=50, blank=False)
    checked_in = models.BooleanField(default=True)
    stay_adults_number = models.IntegerField(null=True, blank=True)
    stay_kids_number = models.IntegerField(null=True, blank=True)
    stay_elderlies_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.fullname