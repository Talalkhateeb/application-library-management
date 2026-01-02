from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserList.as_view(), name='user-list'),
    path('payments/', views.PaymentList.as_view(), name='payment-list'),
    path('ratings/', views.RatingList.as_view(), name='rating-list'),
    path('purchased/', views.PurchasedList.as_view(), name='purchased-list'),
]