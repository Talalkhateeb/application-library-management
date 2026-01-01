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
    is_paid = models.BooleanField(default=False) 
    def save(self, *args, **kwargs):
        if not self.return_date:
            self.return_date = timezone.now().date() + timedelta(days=5)

        if not self.is_paid:
             print("you have to pay for this service ") 
        if not self.pk: 
            if self.book.count > 0:
                self.book.count -= 1
                self.book.save()
            else:
                 raise  ValidationError({
                "error": "this book is not available now",
                "option": " you can reservate the book"
                                        })    
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
    ordering = ['reservation_date']