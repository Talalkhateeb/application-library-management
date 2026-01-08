from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Payment, Purchased, Rating,Book,Borrow,Reservation,Action
from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['status']
class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = '__all__'
        read_only_fields = ['return_date', 'is_paid']
class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['reservation_date', 'is_paid']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "book",
            "type",
            "amount",
            "method",
            "is_success",
            "transaction_id",
            "payment_date"
        ]
        read_only_fields = ["id", "user", "is_success", "transaction_id", "payment_date"]

class PurchasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchased
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'