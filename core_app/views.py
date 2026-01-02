from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics,filters
from .models import Book, Borrow, Action, Reservation,Payment, Purchased, Rating
from .serializers import BookSerializer, BorrowSerializer, ActionSerializer, ReservationSerializer,UserSerializer, PaymentSerializer, PurchasedSerializer, RatingSerializer

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author']
class BorrowList(generics.ListCreateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer

class ActionList(generics.ListCreateAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author']

class ReservationList(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
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