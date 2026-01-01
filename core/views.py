from rest_framework import generics # تأكدي من إضافة هذا السطر
from .user import User
from .payment import Payment
from .purchased import Purchased
from .rating import Rating
from .serializers import UserSerializer, PaymentSerializer, PurchasedSerializer, RatingSerializer

# عرض وإضافة المستخدمين
class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# عرض وإضافة المدفوعات
class PaymentListCreate(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

# عرض وإضافة التقييمات
class RatingListCreate(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

# تعديل أو حذف تقييم محدد
class RatingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer