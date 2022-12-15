from rest_framework import serializers
from guest.models import Guest

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ('id', 'fullname', 'first_name', 'last_name', 'middle_name', 'official_title', 'identification', 'payment_type', 'checked_in', 'stay_adults_number', 'stay_kids_number', 'stay_elderlies_number')