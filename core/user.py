from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    # Methods from usercontroller & userDAO
    def login(self, email, password): pass
    def logout(self): pass
    def check_registration(self): pass
    def update_info(self, user_obj): pass
    def search_book(self): pass
    def get_user(self): pass

class Subscribed(User):
    def login(self, email, password): pass
    def logout(self): pass

class NotSubscribed(User):
    def register(self): pass

class Employee(User):
    e_id = models.IntegerField()
    def login(self, email, password): pass
    def logout(self): pass