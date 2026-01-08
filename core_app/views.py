from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics,filters,status
from .models import Book, Borrow, Action, Reservation,Payment, Purchased, Rating
from .serializers import BookSerializer, BorrowSerializer, ActionSerializer, LoginSerializer, ReservationSerializer,UserSerializer, PaymentSerializer, PurchasedSerializer, RatingSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from decimal import Decimal
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_books(request):
    borrowed = Borrow.objects.filter(user=request.user, is_paid=True, is_returned=False).select_related('book')
    reserved = Reservation.objects.filter(user=request.user, is_paid=True).select_related('book')
    purchased = Purchased.objects.filter(user=request.user).select_related('book')
    
    return Response({
        "borrowed": BookSerializer([b.book for b in borrowed], many=True).data,
        "reserved": BookSerializer([r.book for r in reserved], many=True).data,
        "purchased": BookSerializer([p.book for p in purchased], many=True).data,
    })

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [AllowAny]
    search_fields = ['title', 'author']
class BorrowList(generics.ListCreateAPIView):
    queryset = Borrow.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowSerializer
    def post(self, request):
        book = get_object_or_404(Book, id=request.data['book_id'])
    
        if Borrow.objects.filter(user=request.user, book=book, is_returned=False).exists():
            return Response({"error": "You already borrowed this book"}, status=400)
        if book.count <= 0:
            return Response({"error": "Book not available"}, status=400)
        else:
            op = Borrow.objects.create(user=request.user, book=book)
        serializer = BorrowSerializer(op)
        return Response({
            "status": "OK",
            "borrow": serializer.data,
            "price": book.price
        })

class ActionList(generics.ListCreateAPIView):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author']
class ReservationDetail(generics.RetrieveDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAdminUser]
class ReservationList(generics.ListCreateAPIView):
   permission_classes = [IsAuthenticated]
   queryset = Reservation.objects.all() 
   serializer_class = ReservationSerializer
   def post(self, request):
        book_id = request.data.get("book_id")
        if not book_id:
            return Response({"error": "Book ID is required"}, status=400)

        book = get_object_or_404(Book, id=book_id)

        # Check if the user already reserved this book
        exRes = Reservation.objects.filter(user=request.user, book=book).first()
    
        if exRes:
            if(exRes.is_paid):
                return Response({"error": "You have already reserved this book"}, status=400)
            else:
                exRes.delete()

        # Check if user has reserved 2 or more books
        reserved_count = Reservation.objects.filter(user=request.user).count()
        if reserved_count >= 2:
            return Response({"error": "You cannot reserve more than 2 books"}, status=400)

        # Create the reservation
        reservation = Reservation.objects.create(
            user=request.user,
            book=book
        )

        serializer = ReservationSerializer(reservation)
        return Response({
            "status": "OK",
            "reservation": serializer.data,
            "price": book.price
        })

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class PaymentList(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        book = None
        op_type = request.data['type']
        op_id = request.data['operation_id']

        if op_type == 'borrow':
            operation = get_object_or_404(Borrow, id=op_id, user=request.user)
            operation.is_paid = True
            operation.save()
            book = operation.book

        elif op_type == 'reserve':
            operation = get_object_or_404(Reservation, id=op_id, user=request.user)
            operation.is_paid = True
            operation.save()
            book = operation.book

        elif op_type == 'purchase':
            operation = get_object_or_404(Purchased, id=op_id, user=request.user)
            book = operation.book

        if Decimal(request.data['amount']) != book.price:
            return Response({"error": "Invalid amount"}, status=400)

        is_paid = request.data['method'] != 'cash'

        payment = Payment.objects.create(
            user=request.user,
            book=book,
            amount=book.price,
            method=request.data['method'],
            type=op_type,
            is_paid=is_paid,
            object_id=operation.id
        )


        return Response({"payment_id": payment.id, "status": "OK"})


class PurchasedList(generics.ListCreateAPIView):
    queryset = Purchased.objects.all()
    serializer_class = PurchasedSerializer
    def post(self, request):
        book = get_object_or_404(Book, id=request.data['book_id'])
    
        if book.count <= 0:
            return Response({"error": "Book not available"}, status=400)
        else:
            op = Purchased.objects.create(user=request.user, book=book)
        serializer = PurchasedSerializer(op)
        return Response({
            "status": "OK",
            "purchase": serializer.data,
            "price": book.price
        })
     

class RatingList(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail": "Logged out successfully"})
class MyBorrowsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request): 
        user = request.user
        borrows = Borrow.objects.filter(user=user)
        serializer = BorrowSerializer(borrows, many=True)
        return Response(serializer.data)
class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_obj = User.objects.get(email=serializer.validated_data['email'])
        if not user_obj:
             return Response({"error": "Invalid credentials"}, status=401)
        user = authenticate(
            username = user_obj.username,
            password=serializer.validated_data['password']
        )

      

        if not user:
            return Response({"error": "Invalid credentials"}, status=401)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user_id": user.id,
            "username": user.username,
            "is_staff": user.is_staff,
        })
class ReturnBookView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        user_id = request.data.get('user_id')
        book_id = request.data.get('book_id')

        if not user_id or not book_id:
            return Response(
                {"error": "user_id and book_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        borrow = get_object_or_404(
            Borrow,
            user_id=user_id,
            book_id=book_id,
            is_returned=False,
        )

        book = borrow.book

        # Delete borrow
        borrow.is_returned = True
        borrow.save()

        # Increment book count
        book.count += 1
        book.save()

        return Response(
            {"message": "Book returned successfully"},
            status=status.HTTP_200_OK
        )
