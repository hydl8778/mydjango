from django.contrib import admin
from .models import  CartList,KmList,InsuranceFee,OilFee,ElectricFee,EtcFee,WashFee

# Register your models here.
admin.site.register(CartList)
admin.site.register(KmList)
admin.site.register(InsuranceFee)
admin.site.register(OilFee)
admin.site.register(ElectricFee)
admin.site.register(EtcFee)
admin.site.register(WashFee)