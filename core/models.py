from django.db import models

# Create your models here.

GENDER_CHOICES = (
    ('H','Hombre'),
    ('M','Mujer'),
)

SIZE_CHOICES = (
    ('L','LARGE'),
    ('M','MEDIUM'),
    ('S','SMALL'),
)

COLOR_CHOICES = (
    ('L','LARGE'),
    ('M','MEDIUM'),
    ('S','SMALL'),
)

LABEL_CHOICES = (
    ('N','Nuevo'),
    ('D','Descuento'),
)


class Customer(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=30,blank=True,null=True)
    customer_cookie_id = models.CharField(max_length=128, blank=True, null=True)
    shipping_address = models.ForeignKey(
        'Address',
        related_name='shipping_address_customer',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    billing_address = models.ForeignKey(
        'Address',
        related_name='billing_address_customer',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.name}, {self.last_name}"


class Gender(models.Model):
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1, blank=True, null=True)

    def __str__(self):
        return self.gender


class Category(models.Model):
    name = models.CharField(max_length=64)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.name} de {self.gender.gender}"
    class Meta:
        verbose_name_plural = 'Categories'


class Size(models.Model):
    size = models.CharField(max_length=5, blank=True, null=True)
    def __str__(self): return f"{self.size}"


class Color(models.Model):
    color = models.CharField(max_length=6, blank=True, null=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    def __str__(self): return f"{self.name}"


class CouponOrder(models.Model):
    #customer = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)
    code = models.CharField(max_length=12)
    percentage = models.IntegerField()

    def __str__(self):
        return f"{self.code} | {self.percentage}"


class CouponItem(models.Model):
    #customer = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True)
    code = models.CharField(max_length=12, unique=True)
    percentage = models.IntegerField()

    def __str__(self):
        return self.code


class Item(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    label = models.CharField(choices=LABEL_CHOICES, max_length=2,blank=True, null=True)
    description = models.TextField()
    imageURL1 = models.CharField(max_length=1024, blank=True, null=True);
    imageURL2 = models.CharField(max_length=1024, blank=True, null=True);
    imageURL3 = models.CharField(max_length=1024, blank=True, null=True);
    imageURL4 = models.CharField(max_length=1024, blank=True, null=True);

    def __str__(self):
        return self.name


class ItemVariation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.item.name} | {self.color} | {self.size} | {self.stock}"


class OrderItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    item_variation = models.ForeignKey(ItemVariation, on_delete=models.SET_NULL, blank=True,null=True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    deletion_time = models.DateTimeField(blank=True, null=True)
    total = models.FloatField(blank=True,null=True)
    coupon = models.ForeignKey(
        CouponItem,
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    def __str__(self):
        return f"{self.quantity} de {self.item_variation.item.name} - {self.item_variation.size} | {self.item_variation.color}"


class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        blank=True,null=True
    )
    ref_code = models.CharField(max_length=64)
    order_items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    coupon = models.ForeignKey(
        CouponOrder,
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    total = models.FloatField(blank=True,null=True)
    billing_address = models.ForeignKey(
        'Address',
        related_name='billing_address_order',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    shipping_address = models.ForeignKey(
        'Address',
        related_name='shipping_address_order',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )

    def __str__(self):
        return self.ref_code


class Payment(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        blank=True,null=True
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        blank=True,null=True)
    approved = models.BooleanField(blank=True,null=True)
    pending = models.BooleanField(blank=True,null=True)
    amount = models.FloatField(blank=True,null=True)
    installments = models.IntegerField(blank=True,null=True)
    installment_amount = models.FloatField(blank=True,null=True)
    total_amount = models.FloatField(blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer}"


class Address(models.Model):
    street_name = models.CharField(max_length=64, blank=True, null=True)
    street_number = models.CharField(max_length=64, blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)
    apartment = models.CharField(max_length=5,blank=True, null=True)

    def __str__(self):
        return f"{self.street_name}, {self.street_number}"

    class Meta:
        verbose_name_plural = 'Addresses'
