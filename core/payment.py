from django.db import models
from .user import User

class Payment(models.Model):
    pay_id = models.AutoField(primary_key=True)
    pay_type = models.CharField(max_length=50)
    pay_amount = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Methods from paymentcontroller & PaymentDAO
    def process_payment(self, u_id, amount, pay_type): pass
    def get_invoice(self, p_id): pass
    def add_purchased(self, u_id, book_id): pass