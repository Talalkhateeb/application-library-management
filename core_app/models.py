from django.db import models
from django.contrib.auth.models import User

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

class Action(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    a_type = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

class Reservation(models.Model):
    reservation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
