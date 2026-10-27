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
    service_life = models.IntegerField(verbose_name="报废期限")
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





class OilCost(models.Model):
    cart = models.ForeignKey(
        CartList,
        on_delete=models.PROTECT,           # 有油费记录不许删车
        related_name="oil_costs",
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
    number = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="加油量（升）"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="单价（元）"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name="金额（元）")

    class Meta:
        db_table = 'oil_cost'
        verbose_name = "油费记录"
        verbose_name_plural = verbose_name
        ordering = ['-year', '-month']
        unique_together = ('cart', 'year', 'month')   # 同车同月唯一

    def __str__(self):
        return f"{self.cart.plate_number} {self.year}-{self.month:02d}"



class EtcCost(models.Model):
    cart = models.ForeignKey(
        CartList,
        on_delete=models.PROTECT,
        related_name="etc_costs",
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
    amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="金额（元）"
    )

    class Meta:
        db_table = 'etc_cost'
        verbose_name = "过路费记录"
        verbose_name_plural = verbose_name
        ordering = ['-year', '-month']
        constraints = [
            models.UniqueConstraint(
                fields=['cart', 'year', 'month'],
                name='unique_etc_cart_year_month'
            ),
        ]

    def __str__(self):
        return f"{self.cart.plate_number} {self.year}-{self.month:02d}"






