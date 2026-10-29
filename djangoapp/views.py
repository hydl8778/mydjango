from django.shortcuts import render
from datetime import date
from collections import defaultdict

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from djangoapp.models import CartList, KmList, OilFee, EtcFee, ElectricFee, WashFee, InsuranceFee


class GetAllCartData(APIView):
    """获取车辆所有数据"""
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        year = int(request.query_params.get("year",date.today().year))
        # 1.取出全年数据
        cart_list = CartList.objects.all()
        km_rows = KmList.objects.filter(year=year)
        oil_rows = OilFee.objects.filter(year=year)
        etc_rows = EtcFee.objects.filter(year=year)
        wash_rows = WashFee.objects.filter(year=year)
        insurance_rows = InsuranceFee.objects.filter(year=year)

        # 2.按（cart_id, month）建索引
        km_map = {(r["cart_id"], r["month"]): r["number"] for r in km_rows}
