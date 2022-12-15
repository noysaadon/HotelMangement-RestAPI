from rest_framework import viewsets, status
from rest_framework.response import Response
from account.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, mixins
from account.serializers import MyTokenObtainPairSerializer, RegisterSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
import logging
from datetime import datetime

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
class UserViewSet(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], detail=False)
    def me(self, request, *args, **kwargs):
        User = get_user_model()
        self.object = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class RegisterUser(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try: 
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            logger.warning('Registerd new User on '+str(datetime.now()))
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "message": "User Created. Now perform Login to get your token",
            })

        except:
            message = {'detail': 'User with this email already exists'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

class HotelTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



