from rest_framework import generics
from django.contrib.auth.models import User
from .models import Payment, Purchased, Rating
from .serializers import UserSerializer, PaymentSerializer, PurchasedSerializer, RatingSerializer

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PaymentList(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PurchasedList(generics.ListCreateAPIView):
    queryset = Purchased.objects.all()
    serializer_class = PurchasedSerializer

class RatingList(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer