from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserListCreate.as_view(), name='user-list'),
    path('payments/', views.PaymentListCreate.as_view(), name='payment-list'),
    path('ratings/', views.RatingListCreate.as_view(), name='rating-list'),
    path('ratings/<int:pk>/', views.RatingDetail.as_view(), name='rating-detail'),
]