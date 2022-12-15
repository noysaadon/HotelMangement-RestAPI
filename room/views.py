from datetime import date, datetime, timedelta
from rest_framework import mixins, generics
from rest_framework import viewsets, status
from guest.models import Guest
from room.models import Booking, Discount, FoodCategory, MiniBarPayment, Payment, Room, RoomType
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from room.serializers import BookingDetailSerializer, BookingSerializer, DiscountSerializer, FoodCategorySerializer, MiniBarPaymentDetailSerializer, MiniBarPaymentSerializer, PaymentDetailSerializer, PaymentSerializer, RoomSerializer
from rest_framework.decorators import action
from django.http import Http404
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncDay, TruncYear, TruncWeek, ExtractWeek, ExtractWeekDay, ExtractYear, ExtractMonth, ExtractDay

# Create your views here.
class RoomViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


    def get_queryset(self):
        queryset = Room.objects.all()
        marked_for_booking = self.request.query_params.get('marked_for_booking')
        room_id = self.request.query_params.get('room')
        if marked_for_booking is not None and room_id is not None:
            queryset = queryset.filter(marked_for_booking=marked_for_booking, room_id=room_id)
        elif marked_for_booking is not None:
            queryset = queryset.filter(marked_for_booking=marked_for_booking)
        elif room_id is not None:
            queryset = queryset.filter(room_id=room_id)
        else:
            queryset=queryset
        return queryset

    @action(methods=['get'], detail=False)
    def room_filter(self, request, *args, **kwargs):
        queryset = Room.objects.filter(marked_for_booking=False)
        guest_id = self.request.query_params.get('guest')
        room_type_name = self.request.query_params.get('room_type_name')
        if guest_id is None:
            message = {'detail': 'guest_id is requred'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        elif room_type_name is None:
            message = {'detail': 'room_type_name is requred'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        elif guest_id is not None and room_type_name is not None:
            members = 0
            try:
                guest = Guest.objects.get(id=guest_id)
                if guest.stay_adults_number:
                    members += int(guest.stay_adults_number)
                if guest.stay_kids_number:
                    members += int(guest.stay_kids_number)
                if guest.stay_elderlies_number:
                    members += int(guest.stay_elderlies_number)
                required_room_counters = 0
                if room_type_name == "Regular":
                    required_room_counters =  round(members / 2)
                elif room_type_name == "Premium":
                    required_room_counters =  round(members / 3)
                else:
                    required_room_counters =  round(members / 4)
                room_type_data = RoomType.objects.get(name=room_type_name)
                queryset = queryset.filter(room_type=room_type_data.id)
                serializer = RoomSerializer(queryset, many=True)

            except Exception as e:
                message = {'detail': 'Error existed'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "required_room_counters": required_room_counters,
                "room": serializer.data
            })
        
        else:
            message = {'detail': 'Error Existed'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
                

    def list(self, request):
        queryset = self.get_queryset()
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data)

class BookingViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = Booking.objects.all()
        stay_status = self.request.query_params.get('stay_status')
        room_id = self.request.query_params.get('room')
        if stay_status is not None and room_id is not None:
            queryset = queryset.filter(stay_status=stay_status, room_id=room_id)
        elif stay_status is not None:
            queryset = queryset.filter(stay_status=stay_status)
        elif room_id is not None:
            queryset = queryset.filter(room_id=room_id)
        else:
            queryset=queryset
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = BookingDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args,  **kwargs):
        data = request.data
        
        for room_data in data['room']:
            if Room.objects.get(id=room_data).marked_for_booking:
                return Response({
                    "message": "Alaredy Booked this room"
                })   
            room_book = Room.objects.get(id=room_data)
            room_book.marked_for_booking = True
            room_book.save()        

        if Guest.objects.get(id=data['guest']).checked_in:
            if Booking.objects.filter(guest_id=data['guest']).exclude(stay_status="Leave").exists():
                booking_guest = Booking.objects.get(guest_id=data['guest'])
                return Response({
                    "message": "this Guest Alaredy Booked into " + booking_guest.room.number
                })
        
        room_guest = Guest.objects.get(id=data['guest'])
        room_guest.checked_in = True
        room_guest.save()

        serializer = self.get_serializer(data=data)
        
        try: 
            serializer.is_valid(raise_exception=True)
            booking = serializer.save()
            
            return Response({
                "booking": BookingSerializer(booking, context=self.get_serializer_context()).data,
                "message": "Created Booking.",
            })

        except Exception as e:
            print(e)
            message = {'detail': 'Error existed'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args,  **kwargs):
        instance = self.get_object()
        if request.data.get("stay_status") == "Leave":
            guest_data = instance.guest
            for room_data in request.data.get("room"):
                room_book = Room.objects.get(id=room_data)
                room_book.marked_for_booking = False
                room_book.save()
            guest_data.checked_in = False
            guest_data.save()
        
        try: 
            return super().update(request, *args, **kwargs)

        except:
            message = {'detail': 'Error existed'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            for roomid in instance.room.values('id'):
                room_book = Room.objects.get(id=roomid['id'])
                room_book.marked_for_booking = False
                room_book.save()  
            instance.delete()
        except Http404:
            message = {'detail': 'No Data Found'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

class FoodCategoryViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    queryset = FoodCategory.objects.all()
    serializer_class = FoodCategorySerializer

class DiscountViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer

class PaymentViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PaymentDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try: 
            serializer.is_valid(raise_exception=True)
            payment = serializer.save()
            discount_percent = payment.discount.percent
            room = payment.booking.room.all()
            stay_from = payment.booking.stay_from
            stay_to = payment.booking.stay_to
            delta = stay_to - stay_from
            during = delta.days
            total_amount = 0
            discount_amount = 0
            guest_data = payment.booking.guest
            if guest_data.stay_adults_number:
                total_amount += (int(guest_data.stay_adults_number)) * 150 * (100- float(discount_percent)) / 100
                discount_amount += (int(guest_data.stay_adults_number)) * 150 * (float(discount_percent)) / 100
            if guest_data.stay_kids_number:
                total_amount += (int(guest_data.stay_kids_number)) * 50 * (100 - float(discount_percent)) / 100
                discount_amount += (int(guest_data.stay_kids_number)) * 50 * ( float(discount_percent)) / 100
            if guest_data.stay_elderlies_number:
                total_amount += (int(guest_data.stay_elderlies_number)) * 75 * (100- float(discount_percent)) / 100
                discount_amount += (int(guest_data.stay_elderlies_number)) * 75 * (float(discount_percent)) / 100
                print()

            for room_data in room:
                total_amount += float(room_data.room_type.price)
            payment.total_amount = total_amount * during
            payment.discount_amount = discount_amount * during
            payment.save()

            return Response({
                "payment": PaymentSerializer(payment, context=self.get_serializer_context()).data,
                "message": "Payment Created Successfully.",
            })

        except:
            message = {'detail': 'Error existed'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class MiniBarPaymentViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    queryset = MiniBarPayment.objects.all()
    serializer_class = MiniBarPaymentSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer = MiniBarPaymentDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try: 
            serializer.is_valid(raise_exception=True)
            minibar_payment = serializer.save()
            amount = 0
            if minibar_payment.beer != 0:
                amount += minibar_payment.beer * 20
            if minibar_payment.potato_chips != 0:
                amount += minibar_payment.potato_chips * 10
            if minibar_payment.soda != 0:
                amount += minibar_payment.soda * 15
            if minibar_payment.chocolate_bar != 0:
                amount += minibar_payment.chocolate_bar * 12

            minibar_payment.amount = amount
            minibar_payment.save()
            return Response({
                "minibar-payment": MiniBarPaymentSerializer(minibar_payment, context=self.get_serializer_context()).data,
                "message": "MiniBar Payment Created Successfully.",
            })

        except:
            message = {'detail': 'Error existed'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

class StatisticsViewSet(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        filter_type = self.request.query_params.get('filter_type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if filter_type is not None:
            queryArray = []
            if filter_type == "day":
                queryset = Payment.objects.annotate(date=TruncDay('pay_date')).values('date').annotate(total_amount=Sum('total_amount')).values('date', 'total_amount') 

                queryset_mini = MiniBarPayment.objects.annotate(date=TruncDay('pay_date')).values('date').annotate(total_amount=Sum('amount')).values('date', 'total_amount')
                for query in queryset:
                    queryArray.append(query)
                for query_mini in queryset_mini:
                    queryArray.append(query_mini)
            elif filter_type == "week":
                queryset = Payment.objects.annotate(week=ExtractWeek('pay_date')).values('week').annotate(total_amount=Sum('total_amount')).values('week', 'total_amount') 
                queryset_mini = MiniBarPayment.objects.annotate(week=ExtractWeek('pay_date')).values('week').annotate(total_amount=Sum('amount')).values('week', 'total_amount')
                for query in queryset:
                    queryArray.append(query)
                for query_mini in queryset_mini:
                    queryArray.append(query_mini)
            elif filter_type == "month":
                queryset = Payment.objects.annotate(month=ExtractMonth('pay_date')).values('month').annotate(total_amount=Sum('total_amount')).values('month', 'total_amount') 
                queryset_mini = MiniBarPayment.objects.annotate(month=ExtractMonth('pay_date')).values('month').annotate(total_amount=Sum('amount')).values('month', 'total_amount')
                for query in queryset:
                    queryArray.append(query)
                for query_mini in queryset_mini:
                    queryArray.append(query_mini)
            elif filter_type == "year":
                queryset = Payment.objects.annotate(year=ExtractYear('pay_date')).values('year').annotate(total_amount=Sum('total_amount')).values('year', 'total_amount') 
                queryset_mini = MiniBarPayment.objects.annotate(year=ExtractYear('pay_date')).values('year').annotate(total_amount=Sum('amount')).values('year', 'total_amount')
                for query in queryset:
                    queryArray.append(query)
                for query_mini in queryset_mini:
                    queryArray.append(query_mini)

            return queryArray

        if start_date is not None and end_date is not None:
            queryset = Payment.objects.filter(pay_date__gte=start_date, pay_date__lte=end_date).annotate(date=TruncDay('pay_date')).values('date').annotate(total_amount=Sum('total_amount')).values('date', 'total_amount') 

            return queryset
        today = date.today()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)

        queryset = Payment.objects.filter(pay_date__gte=start, pay_date__lte=end).annotate(date=TruncDay('pay_date')).values('date').annotate(total_amount=Sum('total_amount')).values('date', 'total_amount') 

        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        
        return Response(queryset)

class StatisticsMiniBarViewSet(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = MiniBarPaymentSerializer

    def get_queryset(self):
        filter_type = self.request.query_params.get('filter_type')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if filter_type is not None:
            if filter_type == "day":
                queryset = MiniBarPayment.objects.annotate(date=TruncDay('pay_date')).values('date').annotate(total_amount=Sum('amount')).values('date', 'total_amount')
            elif filter_type == "week": 
                queryset = MiniBarPayment.objects.annotate(week=ExtractWeek('pay_date')).values('week').annotate(total_amount=Sum('amount')).values('week', 'total_amount')
                
            elif filter_type == "month":
                queryset = MiniBarPayment.objects.annotate(month=ExtractMonth('pay_date')).values('month').annotate(total_amount=Sum('amount')).values('month', 'total_amount')
            elif filter_type == "year":
                queryset = MiniBarPayment.objects.annotate(year=ExtractYear('pay_date')).values('year').annotate(total_amount=Sum('amount')).values('year', 'total_amount')

            return queryset

        if start_date is not None and end_date is not None:
            queryset = MiniBarPayment.objects.filter(pay_date__gte=start_date, pay_date__lte=end_date).annotate(date=TruncDay('pay_date')).values('date').annotate(total_amount=Sum('amount')).values('date', 'total_amount') 

            return queryset
        today = date.today()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)

        queryset = MiniBarPayment.objects.filter(pay_date__gte=start, pay_date__lte=end).annotate(date=TruncDay('pay_date')).values('date').annotate(total_amount=Sum('amount')).values('date', 'total_amount') 

        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        
        return Response(queryset)