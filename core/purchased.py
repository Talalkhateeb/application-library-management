from django.db import models
from .user import User

class Purchased(models.Model):
    purchased_id = models.AutoField(primary_key=True)
    purchase_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.IntegerField() # معرف الكتاب من فئة Book

    # Logic from Diagram
    def add_to_history(self): pass