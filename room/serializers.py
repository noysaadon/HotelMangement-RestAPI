from rest_framework import serializers
from guest.models import Guest
from guest.serializers import GuestSerializer
from room.models import Booking, Discount, FoodCategory, MiniBarPayment, Payment, PaymentMode, Room, RoomType

class RoomSerializer(serializers.ModelSerializer):
    room_type = serializers.SlugRelatedField(queryset=RoomType.objects.all(), slug_field='name')

    class Meta:
        model = Room
        fields = ['id','number', 'room_type', 'marked_for_booking']

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ('id', 'room', 'guest', 'stay_from', 'stay_to','stay_status')

class BookingDetailSerializer(serializers.ModelSerializer):
    room = RoomSerializer(many=True, read_only=False)
    guest = GuestSerializer(many=False)
    stay_day = serializers.SerializerMethodField(method_name=None)

    class Meta:
        model = Booking
        fields = ['id', 'room', 'guest', 'stay_from', 'stay_to','stay_status','stay_day']

    def get_stay_day(self, obj):
        if obj.stay_from and obj.stay_to:
            delta = obj.stay_to - obj.stay_from
            return delta.days
        else:
            return 0

class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ('id','name', 'price_per')

class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discount
        fields = ('id', 'name', 'percent')

class PaymentModeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMode
        fields = ('id', 'name')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'booking', 'discount')

class PaymentDetailSerializer(serializers.ModelSerializer):
    booking = BookingSerializer(many=False)
    discount = DiscountSerializer(many=False)

    class Meta:
        model = Payment
        fields = ('id', 'booking', 'total_amount', 'discount','discount_amount')

class MiniBarPaymentDetailSerializer(serializers.ModelSerializer):
    room = RoomSerializer(many=False)
    class Meta:
        model = MiniBarPayment
        fields = ('id', 'room', 'beer', 'potato_chips', 'soda', 'chocolate_bar', 'amount')

class MiniBarPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiniBarPayment
        fields = ('id', 'room', 'beer', 'potato_chips', 'soda', 'chocolate_bar')