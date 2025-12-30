from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    b_year = models.IntegerField()
    status = models.CharField(max_length=50)
    count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if self.count <= 0:
            self.status = "Not Available"
        else:
            self.status = "Available"
        
        super().save(*args, **kwargs)

class Borrow(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False) # تأكدي من تفعيل السطر

    def save(self, *args, **kwargs):
        # الحل: نستخدم تاريخ اليوم الحالي مباشرة للحساب
        if not self.return_date:
            self.return_date = timezone.now().date() + timedelta(days=5)

        # 2. التحقق من الدفع (للتجربة حالياً اجعليها تعطي تنبيه فقط أو عطليه مؤقتاً)
        if not self.is_paid:
             print("تنبيه: لم يتم الدفع") # لكي لا يتوقف الـ API عن العمل الآن

        # 3. منطق نقص الكتب
        if not self.pk: 
            if self.book.count > 0:
                self.book.count -= 1
                self.book.save()
            else:
                 raise  ValidationError({
                "error": "هذا الكتاب غير متوفر حالياً للاستعارة.",
                "option": "يمكنك تسجيل طلب حجز (Reservation) لتكون لك الأولوية عند توفر الكتاب."
                                        })    
        super().save(*args, **kwargs)
class Action(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    a_type = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

class Reservation(models.Model):
    reservation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    # في models.py داخل كلاس Reservation
    class Meta:
        ordering = ['reservation_date'] # الأقدم (أول من حجز) يظهر في الأعلى