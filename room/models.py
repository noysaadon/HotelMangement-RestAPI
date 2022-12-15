import datetime
from django.db import models
import uuid
from guest.models import Guest

# Create your models here.
class RoomType(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default = uuid.uuid4)
    name = models.CharField(max_length=100 ,blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    price = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Room(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default = uuid.uuid4)
    number = models.CharField(max_length=100, blank=False, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    marked_for_booking = models.BooleanField(default=False)

    def __str__(self):
        return self.number


class Discount(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default = uuid.uuid4)
    name = models.CharField(max_length=50, blank=False, unique=True)
    percent = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.name}'


class Booking(models.Model):

    BOOKING_STATUS_CHOICES = (
        ('STAY', 'STAY'),
        ('EXTEN', 'EXTENSION'),
        ('SHORT', "SHORTENING"),
        ('LEAVE', 'LEAVE'),
    )
    id = models.UUIDField(primary_key=True, editable=False, default = uuid.uuid4)
    room = models.ManyToManyField(Room, related_name="rooms")
    guest = models.ForeignKey(Guest,related_name="guests", on_delete=models.CASCADE)
    stay_from = models.DateTimeField()
    stay_to = models.DateTimeField()
    stay_status = models.CharField( max_length=5, default='STAY', choices=BOOKING_STATUS_CHOICES)
    
    def __str__(self):
        return f'{self.guest.fullname}'


class FoodCategory(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default = uuid.uuid4)
    name = models.CharField(max_length=100)
    price_per = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class PaymentMode(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default = uuid.uuid4)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default = uuid.uuid4)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    discount = models.ForeignKey(Discount, blank=True, null=True, on_delete=models.SET_NULL)
    discount_amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    pay_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f'{self.booking.guest.fullname}'


class MiniBarPayment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default = uuid.uuid4)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    beer = models.IntegerField()
    potato_chips = models.IntegerField(default=0)
    soda = models.IntegerField(default=0)
    chocolate_bar = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pay_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f'{self.room.number}'