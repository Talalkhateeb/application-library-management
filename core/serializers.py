from rest_framework import serializers
from .user import User, Subscribed, Employee
from .payment import Payment
from .purchased import Purchased
from .rating import Rating

# 1. محول بيانات المستخدم (يتعامل مع الوراثة)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        # حماية كلمة المرور لكي لا تظهر عند عرض البيانات (للكتابة فقط)
        extra_kwargs = {'password': {'write_only': True}}

# 2. محول بيانات الدفع
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

# 3. محول بيانات المشتريات
class PurchasedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchased
        fields = '__all__'
        # تحديد حقل التاريخ كقراءة فقط لكي لا يغيره المستخدم يدويًا
        read_only_fields = ['purchase_date']

# 4. محول بيانات التقييم
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'