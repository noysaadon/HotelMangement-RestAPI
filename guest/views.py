from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets, status
from guest.models import Guest
from rest_framework.permissions import IsAuthenticated

from guest.serializers import GuestSerializer

# Create your views here.


class GuestViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
