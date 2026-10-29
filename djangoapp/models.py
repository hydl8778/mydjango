from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CartList(models.Model):
    """车辆固定参数"""

    plate_number = models.CharField(max_length=32, unique=True, verbose_name="车牌")

    oil_card = models.CharField(max_length=32, null=True, blank=True, verbose_name="加油卡号")
    etc_card = models.CharField(max_length=32, null=True, blank=True,verbose_name="粤通卡号")

    admin = models.CharField(max_length=32, null=True, blank=True, verbose_name="车辆管理员")

    power_type = models.CharField(max_length=16, null=True, blank=True, verbose_name="动力类型")
    oil_number = models.CharField(max_length=16, null=True, blank=True,verbose_name="油号")

    category = models.CharField(max_length=32, null=True, blank=True, verbose_name="车辆类别")
    brand_model = models.CharField(max_length=64, null=True, blank=True, verbose_name="品牌型号")
    purchase_date = models.DateField(null=True, blank=True, verbose_name="购置日期")
    service_life = models.IntegerField(default=15, verbose_name="报废期限")
    use_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="车船税")
    check_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="年检费")
    insurance_start = models.DateField(null=True, blank=True, verbose_name="保险开始日期")
    insurance_end = models.DateField(null=True, blank=True, verbose_name="保险结束日期")

    class Meta:
        db_table = 'cart_list'
        verbose_name = "车辆信息"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.plate_number

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.insurance_start and self.insurance_end \
                and self.insurance_end < self.insurance_start:
            raise ValidationError("保险结束日期不能早于开始日期")



class BaseFee(models.Model):
    cart = models.ForeignKey(CartList, on_delete=models.PROTECT, related_name="%(class)ss", verbose_name="车辆")
    year = models.IntegerField( validators=[MinValueValidator(1900), MaxValueValidator(2100)], verbose_name="年份")
    month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)], verbose_name="月份")
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0, verbose_name="金额（元）")

    class Meta:
        abstract = True
        ordering = ["-year", "-month"]


    def __str__(self):
        return f"{self.cart.plate_number} {self.year}-{self.month:02d}"


class KmList(models.Model):
    cart = models.ForeignKey(
        CartList,
        on_delete=models.PROTECT,          # 有里程记录不许删车（和其他费用模型统一）
        related_name="km_lists",           # ✅ 英文反向名
        verbose_name="车辆"
    )
    year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        verbose_name="年份"
    )
    month = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name="月份"
    )
    number = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="里程（km）"
    )

    class Meta:
        db_table = "km_list"
        verbose_name = "表盘里程记录"
        verbose_name_plural = verbose_name
        ordering = ["-year", "-month"]
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "year", "month"],
                name="unique_km_cart_year_month"
            )
        ]

    def __str__(self):
        return f"{self.cart.plate_number} {self.year}-{self.month:02d}"

class InsuranceFee(models.Model):
    cart = models.ForeignKey(
        CartList,
        on_delete=models.PROTECT,
        related_name="insurance_fees",          # ✅ 复数
        verbose_name="车辆"
    )
    year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
        verbose_name="年份"
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2,        # ✅ 补上，否则报错
        validators=[MinValueValidator(0)],
        verbose_name="保险费（元）"
    )

    class Meta:
        db_table = "insurance_fee"
        verbose_name = "保险费记录"
        verbose_name_plural = verbose_name
        ordering = ["-year"]
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "year"],
                name="unique_insurance_fee_year"
            )
        ]

    def __str__(self):
        return f"{self.cart.plate_number} {self.year}年保险"


class OilFee(BaseFee):

    number = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)], verbose_name="加油量（升）"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,validators=[MinValueValidator(0)], verbose_name="单价（元）"
    )
    class Meta(BaseFee.Meta):
        db_table = 'oil_fee'
        verbose_name = "油费记录"
        verbose_name_plural = verbose_name
        ordering = ['-year', '-month']
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'year', 'month'],
                name='unique_oil_fee_year_month'
            ),
        ]



class ElectricFee(BaseFee):
    number = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,validators=[MinValueValidator(0)], verbose_name="电量（kwh）"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,validators=[MinValueValidator(0)], verbose_name="单价（元）"
    )

    class Meta(BaseFee.Meta):
        db_table = 'electric_fee'
        verbose_name = "充电费记录"
        verbose_name_plural = verbose_name
        ordering = ['-year', '-month']
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'year', 'month'],
                name='unique_electric_fee_year_month'
            ),
        ]



class EtcFee(BaseFee):
    class Meta(BaseFee.Meta):
        db_table = 'etc_fee'
        verbose_name = "过路费记录"
        verbose_name_plural = verbose_name
        ordering = ['-year', '-month']
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'year', 'month'],
                name='unique_etc_fee_year_month'
            ),
        ]


class WashFee(BaseFee):
    class Meta(BaseFee.Meta):
        db_table = 'wash_fee'
        verbose_name = "洗车费记录"
        verbose_name_plural = verbose_name
        ordering = ['-year', '-month']
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'year', 'month'],
                name='unique_wash_fee_year_month'
            ),
        ]




