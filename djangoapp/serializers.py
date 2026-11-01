from rest_framework import serializers

from djangoapp.models import OilFee


class OilFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OilFee
        fields = '__all__'