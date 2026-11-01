from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from djangoapp.views import GetAllCartData, GetOil

router = DefaultRouter()
router.register("oil", GetOil, basename="oil")   # GetOil 是 ModelViewSet

urlpatterns = [
    path('cart_all/', GetAllCartData.as_view(), name='cart_all'),  # APIView
] + router.urls                                   # 合并，不是覆盖