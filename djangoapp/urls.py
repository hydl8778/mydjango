from django.contrib import admin
from django.urls import path

from djangoapp.views import GetAllCartData

urlpatterns = [
    path('cart_all/', GetAllCartData.as_view(), name='cart_all'),
]