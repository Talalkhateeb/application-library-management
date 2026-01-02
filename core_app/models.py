from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# كلاس الشراء بنفس منطق الاستعارة الخاص بكِ
class Purchased(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.pk: # عند الإنشاء فقط
            if self.book.count > 0:
                self.book.count -= 1
                self.book.save()
                self.price_at_purchase = self.book.price
            else:
                raise ValidationError("This book is out of stock.")
        super().save(*args, **kwargs)

# كلاس الدفع
class Payment(models.Model):
    PAYMENT_METHODS = [('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('cash', 'Cash')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    is_success = models.BooleanField(default=True)

# كلاس التقييم مع التحقق من الدرجة
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    score = models.IntegerField(default=5)
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.score < 1 or self.score > 5:
            raise ValidationError("Rating must be between 1 and 5.")