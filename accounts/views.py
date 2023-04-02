from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .models import User


from .serializers import UserSerializer


class LogoutAPIView(APIView):
    pass


class UserRegistration(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
