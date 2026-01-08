from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
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
     is_new = self.pk is None
    
     if self.count <= 0:
        self.status = "Not Available"
     else:
        self.status = "Available"
    
     super().save(*args, **kwargs)
     if is_new:
        admin_user = User.objects.filter(is_staff=True).first()
        if admin_user:
            Action.objects.create(
                book=self,
                employee=admin_user,
                a_type='add'
            )
class Borrow(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_returned = models.BooleanField(default=False) 
    is_paid = models.BooleanField(default=False) 
    def save(self, *args, **kwargs):
        if not self.return_date:
            self.return_date = timezone.now().date() + timedelta(days=5)
        if not self.pk: 
         
            if self.is_paid:
                self.book.count -= 1
                self.book.save()
        else:
            orig = Borrow.objects.get(pk=self.pk)
            if not orig.is_paid and self.is_paid:
                self.book.count-=1
                self.book.save()
        super().save(*args, **kwargs)
class Action(models.Model):
    ACTION_CHOICES = [
        ('add', 'add a new book'),
        ('delete','delete a book'),
        ('update', 'update book ')
    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    a_type = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name="action type"
    )
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.get_a_type_display()} - {self.book.title}"

class Reservation(models.Model):
    reservation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False) 
    class Meta:
        ordering = ['reservation_date']
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

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('cash', 'Cash')
    ]

    PAYMENT_TYPES = [
        ('borrow', 'Borrow'),
        ('reserve', 'Reserve'),
        ('purchase', 'Purchase'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book,null=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    type = models.CharField(max_length=20, null=True, choices=PAYMENT_TYPES)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    score = models.IntegerField(default=5)
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.score < 1 or self.score > 5:
            raise ValidationError("Rating must be between 1 and 5.")

class UserProfile(models.Model):
  
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def str(self):
        return self.user.username 