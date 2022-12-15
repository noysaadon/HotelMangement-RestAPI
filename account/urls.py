from django.urls import path
from account.views import RegisterUser

urlpatterns = [
    path('users/register/', RegisterUser.as_view(), name='register'),
]