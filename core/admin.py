from django.contrib import admin
from . models import (
    Customer,
    Gender,
    Category,
    Size,
    Color,
    CouponOrder,
    CouponItem,
    Item,
    ItemVariation,
    OrderItem,
    Order,
    Payment,
    Address,
)

class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'last_name',
        'phone_number',
        'shipping_address',
        'billing_address',
        'customer_cookie_id'
    ]


class GenderAdmin(admin.ModelAdmin):
    list_display = [
        'gender'
    ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'gender'
    ]


class SizeAdmin(admin.ModelAdmin):
    list_display = [
        'size',
    ]


class ColorAdmin(admin.ModelAdmin):
    list_display = [
        'color',
        'name'
    ]


class CouponOrderAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'percentage'
    ]

class CouponItemAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'percentage'
    ]

class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'price',
        'discount_price',
        'category',
        'label',
    ]

class ItemVariationAdmin(admin.ModelAdmin):
    list_display = [
        'item',
        'size',
        'color',
        'stock',
    ]


class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        'customer',
        'item_variation',
        'ordered',
        'quantity',
        'total',
        'coupon'
    ]

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'ref_code',
        'customer',
        'ordered',
        'coupon',
        'being_delivered',
        'received',
        'total',
        'billing_address',
        'shipping_address'
    ]

class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'order',
        'customer',
        'approved',
        'pending',
        'amount',
        'installments',
        'installment_amount',
        'total_amount',
        'timestamp',
    ]

class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'street_name',
        'street_number',
        'floor',
        'apartment',
    ]

# ---------------------------------------- #
# ---------------------------------------- #

admin.site.register(Customer,CustomerAdmin)

admin.site.register(Gender,GenderAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Color,ColorAdmin)

admin.site.register(CouponOrder,CouponOrderAdmin)
admin.site.register(CouponItem,CouponItemAdmin)

admin.site.register(Item,ItemAdmin)
admin.site.register(ItemVariation,ItemVariationAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Order,OrderAdmin)

admin.site.register(Payment,PaymentAdmin)
admin.site.register(Address,AddressAdmin)
