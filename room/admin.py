from django.contrib import admin
from room.models import Booking, Discount, MiniBarPayment, Payment, PaymentMode, Room, RoomType, FoodCategory
# Register your models here.

admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Discount)
admin.site.register(Booking)
admin.site.register(FoodCategory)
admin.site.register(PaymentMode)
admin.site.register(Payment)
admin.site.register(MiniBarPayment)