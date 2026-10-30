from django.shortcuts import render
from datetime import date
from collections import defaultdict

from rest_framework import response
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
        electric_rows = ElectricFee.objects.filter(year=year)

        # 2.按（cart_id, month）建索引
        insurance_map = {r.cart_id: r.amount for r in insurance_rows}
        km_map = {(r.cart_id, r.month): r.number for r in km_rows}
        oil_map = {(r.cart_id, r.month): (r.amount, r.number, r.price)  for r in oil_rows}
        etc_map = {(r.cart_id, r.month): r.amount  for r in etc_rows}
        wash_map = {(r.cart_id, r.month): r.amount  for r in wash_rows}
        electric_map = {(r.cart_id, r.month): (r.amount, r.number, r.price)  for r in electric_rows}

        # 3.构建行数据
        rows = []
        for cart in cart_list:
            row = {"plate_number": cart.plate_number,
                    "oil_card": cart.oil_card,
                    "etc_card": cart.etc_card,
                    "admin": cart.admin,
                    "power_type": cart.power_type,
                    "oil_number": cart.oil_number,
                    "category": cart.category,
                    "brand_model": cart.brand_model,
                    "purchase_date": cart.purchase_date,
                    "service_life": cart.service_life,
                    "use_tax": cart.use_tax,
                    "check_fee": cart.check_fee,
                    "insurance_start": cart.insurance_start,
                    "insurance_end": cart.insurance_end,
                    "img": cart.img.url if cart.img else None,
                    }
            for m in range(1, 13):
                row[f"km_{m}"] = km_map.get((cart.id, m), 0)
                oil_0, oil_1, oil_2 = oil_map.get((cart.id, m),  (0, 0, 0))
                row[f"oil_amount_{m}"] = oil_0
                row[f"oil_number_{m}"] = oil_1
                row[f"oil_price_{m}"] = oil_2
                row[f"etc_amount_{m}"] = etc_map.get((cart.id, m), 0)
                row[f"wash_amount_{m}"] = wash_map.get((cart.id, m), 0)
                electric_0, electric_1, electric_2 = electric_map.get((cart.id, m),  (0, 0, 0))
                row[f"electric_amount_{m}"] = electric_0
                row[f"electric_number_{m}"] = electric_1
                row[f"electric_price_{m}"] = electric_2
            row["insurance"] = insurance_map.get(cart.id, 0)
            rows.append(row)
        return Response({
                "year": year,
                "rows": rows,
        })