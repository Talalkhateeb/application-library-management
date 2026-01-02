"""
URL configuration for library_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from core_app import views
from core_app.views import BookList, BorrowList,ReservationList,ActionList,BookDetail,UserList,PaymentList,RatingList,PurchasedList
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/books/', BookList.as_view()),
    path('api/borrows/', BorrowList.as_view()),
    path('api/reservation/',ReservationList.as_view()),
    path('api/action/',ActionList.as_view(),name='action-list'),
    path('api/book/<int:pk>/',BookDetail.as_view(),name='book_detail'),
    path('users/', UserList.as_view(), name='user-list'),
    path('payments/', PaymentList.as_view(), name='payment-list'),
    path('ratings/', RatingList.as_view(), name='rating-list'),
    path('purchased/',PurchasedList.as_view(), name='purchased-list')]

