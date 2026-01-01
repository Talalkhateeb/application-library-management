from django.shortcuts import render

from rest_framework import generics,filters
from .models import Book, Borrow, Action, Reservation
from .serializers import BookSerializer, BorrowSerializer, ActionSerializer, ReservationSerializer

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