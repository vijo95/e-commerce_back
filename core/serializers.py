from rest_framework import serializers

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
    Address
)

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id','name','last_name',
            'email','phone_number',
            'customer_cookie_id',
        ]


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id','gender']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','gender']


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id','size']

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id','color']


class CouponOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponOrder
        fields = ['id','code','percentage']


class CouponItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponItem
        fields = ['id','code','percentage']


class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    gender = serializers.ReadOnlyField(source='category.gender.gender')
    class Meta:
        model = Item
        fields = [
            'id','name','price',
            'discount_price',
            'gender',
            'category',
            'category_name',
            'label',
            'description',
            'imageURL1','imageURL2',
            'imageURL3','imageURL4',
        ]


class ItemVariationSerializer(serializers.ModelSerializer):
    color_name = serializers.ReadOnlyField(source='color.color')
    size_name = serializers.ReadOnlyField(source='size.size')
    class Meta:
        model = ItemVariation
        fields = [
            'id','item',
            'size','color',
            'stock',
            'color_name',
            'size_name',
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    size = serializers.ReadOnlyField(source='item_variation.size.size')
    color = serializers.ReadOnlyField(source='item_variation.color.name')
    name = serializers.ReadOnlyField(source='item_variation.item.name')
    imgURL = serializers.ReadOnlyField(source='item_variation.item.imageURL1')
    class Meta:
        model = OrderItem
        fields = [
            'id','customer',
            'ordered','coupon',
            'item_variation',
            'size','color',
            'name','quantity',
            'total','imgURL',
        ]


class OrderSerializer(serializers.ModelSerializer):
    coupon_code = serializers.ReadOnlyField(source='coupon.code')
    coupon_percentage = serializers.ReadOnlyField(source='coupon.percentage')
    class Meta:
        model = Order
        fields = [
            'id','customer',
            'ref_code','order_items',
            'ordered','coupon',
            'coupon_code',
            'coupon_percentage',
            'being_delivered',
            'received','total',
            'shipping_address',
            'billing_address'
        ]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id','order',
            'customer','amount',
            'total_installment',
            'installments',
            'total_amount',
            'timestamp',
        ]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id','street_name',
            'street_number',
            'floor','apartment',
        ]
