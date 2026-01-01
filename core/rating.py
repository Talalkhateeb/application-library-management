from django.db import models
from .user import User

class Rating(models.Model):
    rate_id = models.AutoField(primary_key=True)
    score = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.IntegerField()

    # Methods from ratingDAO
    def add_rating(self, u_id, book_id, score): pass
    def get_rating_avg(self, book_id): pass