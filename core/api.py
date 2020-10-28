from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from datetime import date
import random
import string
import mercadopago
import datetime
from django.utils import timezone

from . models import (
    Customer,
    Gender,
    Category,
    CouponOrder,
    CouponItem,
    Item,
    ItemVariation,
    OrderItem,
    Order,
    Payment,
    Address
)

from . serializers import (
    CustomerSerializer,
    GenderSerializer,
    CategorySerializer,
    SizeSerializer,
    ColorSerializer,
    CouponOrderSerializer,
    CouponItemSerializer,
    ItemSerializer,
    ItemVariationSerializer,
    OrderItemSerializer,
    OrderSerializer,
    PaymentSerializer,
    AddressSerializer
)

from django.conf import settings

mp = mercadopago.MP(settings.MERCADOPAGO_SECRET_KEY)

def create_ref_code():
    return ''.join(random.choices(
        string.ascii_lowercase + string.digits,
        k=random.randint(32,64)))


class NewCustomerAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        customer_cookie_id = request.data.get('customer_cookie_id', None)
        customer = Customer.objects.create(
            customer_cookie_id=customer_cookie_id
        )
        customer.save()

        return Response(
            {'message':'New Customer'},
            status=HTTP_200_OK
        )

# ---------------------------------------- #

class HomeItemsAPIView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):

        home_item_list = []
        for home_item in Item.objects.all().order_by('-label')[:12]:
            home_item_list.append(ItemSerializer(home_item).data)

        context = {
            'home_item_list': home_item_list
        }

        return Response(context,status=HTTP_200_OK)


class AllItemsAPIView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):

        all_item_list = []
        for item in Item.objects.all().order_by('-label'):
            all_item_list.append(ItemSerializer(item).data)

        context = {
            'all_item_list': all_item_list
        }

        return Response(context,status=HTTP_200_OK)


class CategoriesAPIView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):

        categories = []
        for cat in Category.objects.all().order_by('gender__gender'):
            categories.append(CategorySerializer(cat).data)

        context = {
            'categories': categories
        }

        return Response(context,status=HTTP_200_OK)


class ItemVariationsAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        try:
            item_id = request.data.get("item_id", None)
            item = Item.objects.get(id=item_id)
            item_variation_list = []

            now_time = timezone.now()
            for order_item in OrderItem.objects.filter(ordered=False):
                if order_item.deletion_time <= now_time:
                    customer = order_item.customer
                    order = Order.objects.get(customer=customer,ordered=False)
                    item_variation = order_item.item_variation

                    item_variation.stock += order_item.quantity
                    item_variation.save()
                    order.total -= order_item.total
                    order.save()

                    order_item.delete()


            for item_variation in ItemVariation.objects.filter(item=item):
                item_variation_list.append(ItemVariationSerializer(item_variation).data)

            context = {
                'item_variations': item_variation_list
            }

            return Response(context,status=HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)

# ---------------------------------------- #

class CustomerOrderAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        try:
            customer_cookie_id = request.data.get("customer_cookie_id", None)
            customer = Customer.objects.get(customer_cookie_id=customer_cookie_id)

            order = Order.objects.get(customer=customer, ordered=False)

            order_items_list = []
            for order_item in OrderItem.objects.filter(customer=customer,ordered=False).order_by('-id'):
                order_items_list.append(OrderItemSerializer(order_item).data)


            context = {
                "order": OrderSerializer(order).data,
                "order_items_list": order_items_list
            }

            return Response(context,status=HTTP_200_OK)
        except Exception as e:
            print(e)
            order_items_list = []
            context = {
                "order": None,
                "order_items_list": order_items_list
            }
            return Response(context,status=HTTP_200_OK)


class AddItemToCartAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        try:
            #data fetch from client to add item to cart
            customer_cookie_id = request.data.get('customer_cookie_id', None)
            item_id = request.data.get('item_id', None)
            color = request.data.get('color')
            size = request.data.get('size')
            quantity = request.data.get('quantity')


            # customer obj and item obj
            customer = Customer.objects.get(customer_cookie_id=customer_cookie_id)
            item = Item.objects.get(id=item_id)

            # customer order
            order_qs = Order.objects.filter(customer=customer,ordered=False)
            item_variation = ItemVariation.objects.get(item=item,size=size,color=color)
            if(quantity <= item_variation.stock):
                item_variation.stock -= quantity
                item_variation.save()

            # item variation to check if is already in order
            item_variation = ItemVariation.objects.get(item=item,color=color,size=size)
            if item.discount_price != None:
                item_price = round(item.discount_price,2)
            else:
                item_price = round(item.price,2)

            # check if customer has an order and add the item
            if order_qs.exists():
                order = order_qs[0]
                order_items_list = order.order_items.all()
                for oi in order_items_list:
                    if(oi.item_variation == item_variation):
                        oi.quantity += quantity
                        oi.total += round(quantity*item_price,2)
                        oi.save()
                        order.total += round(quantity*item_price,2)
                        order.save()
                        return Response(
                            {'message':'Item Added 1'},
                            status=HTTP_200_OK
                        )
                # create OrderItem obj
                creation_time = datetime.datetime.now()
                hours = datetime.timedelta(hours = 1)
                deletion_time = creation_time + hours
                order_item = OrderItem.objects.create(
                    customer=customer,
                    item_variation=item_variation,
                    ordered=False,
                    quantity=quantity,
                    deletion_time=deletion_time,
                    total=item_price*quantity,
                )
                order_item.save()
                order.order_items.add(order_item)
                print(order_item.total)
                order.total += round(order_item.total,2)
                order.save()
                return Response(
                    {'message':'Item Added 2'},
                    status=HTTP_200_OK
                )
            else:
                # create OrderItem obj
                creation_time = datetime.datetime.now()
                hours = datetime.timedelta(hours = 1)
                deletion_time = creation_time + hours
                order_item = OrderItem.objects.create(
                    customer=customer,
                    item_variation=item_variation,
                    ordered=False,
                    quantity=quantity,
                    deletion_time=deletion_time,
                    total=item_price*quantity
                )
                order_item.save()

                order = Order.objects.create(
                    customer=customer,
                    ref_code=create_ref_code(),
                    ordered=False,
                    being_delivered=False,
                    received=False,
                    total=order_item.total
                )
                order.order_items.add(order_item)
                order.save()


            return Response(
                {'message':'Item Added 3'},
                status=HTTP_200_OK
            )


        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)


class DeleteItemFromCartAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        try:
            order_item_id = request.data.get("order_item_id", None)
            customer_cookie_id = request.data.get("customer_cookie_id", None)

            order_item = OrderItem.objects.get(id=order_item_id)
            customer = Customer.objects.get(customer_cookie_id=customer_cookie_id)
            order = Order.objects.get(customer=customer,ordered=False)
            item_variation = order_item.item_variation

            item_variation.stock += order_item.quantity
            item_variation.save()
            order.total -= order_item.total
            if order.total < 0:
                order.total = 0
            order.save()

            OrderItem.objects.get(id=order_item_id).delete()

            return Response(
                {"message":"Item Deleted"},
                status=HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)


class AddOneItemAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        order_item_id = request.data.get("order_item_id", None)
        item_variation_id = request.data.get("item_variation_id", None)
        order_id = request.data.get("order_id", None)
        try:
            order_item = OrderItem.objects.get(id=order_item_id)
            item_variation = ItemVariation.objects.get(id=item_variation_id)
            order = Order.objects.get(id=order_id)

            if 0 < item_variation.stock:
                price = order_item.total / order_item.quantity
                item_variation.stock -= 1
                item_variation.save()
                order_item.quantity += 1
                order_item.total += price
                order_item.save()
                order.total += price
                order.save()
                return Response({"message":"ok"},status=HTTP_200_OK)

            return Response({"message":"no stock"},status=HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)


class DeleteOneItemAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        order_item_id = request.data.get("order_item_id", None)
        item_variation_id = request.data.get("item_variation_id", None)
        order_id = request.data.get("order_id", None)

        try:
            order_item = OrderItem.objects.get(id=order_item_id)
            item_variation = ItemVariation.objects.get(id=item_variation_id)
            order = Order.objects.get(id=order_id)

            if 2 <= order_item.quantity:
                price = order_item.total / order_item.quantity
                item_variation.stock += 1
                item_variation.save()
                order_item.total -= price
                order_item.quantity -= 1
                order_item.save()
                order.total -= price
                order.save()
                return Response({"message":"ok"},status=HTTP_200_OK)
            else:
                price = order_item.total / order_item.quantity
                item_variation.stock += 1
                item_variation.save()
                OrderItem.objects.get(id=order_item_id).delete()
                order.total -= price
                order.save()
                return Response({"message":"ok"},status=HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)

# ---------------------------------------- #

class CustomerInfoAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        try:
            customer_cookie_id = request.data.get("customer_cookie_id", None)
            customer = Customer.objects.get(customer_cookie_id=customer_cookie_id)

            default_shipping_address = customer.shipping_address
            default_billing_address = customer.billing_address

            if default_shipping_address != None and default_billing_address != None:
                context = {
                    'default_shipping_address': AddressSerializer(default_shipping_address).data,
                    'default_billing_address': AddressSerializer(default_billing_address).data
                }
            else:
                context = {
                    'default_shipping_address': None,
                    'default_billing_address': None
                }

            return Response(context,status=HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)


class SubmitCheckoutAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        customer_cookie_id = request.data.get("customer_cookie_id", None)

        name = request.data.get("name", None)
        last_name = request.data.get("last_name", None)
        phone = request.data.get("phone", None)
        email = request.data.get("email", None)

        shipping_street_name = request.data.get("shipping_street_name", None)
        shipping_street_number = request.data.get("shipping_street_number", None)
        shipping_floor = request.data.get("shipping_floor", None)
        shipping_apartment = request.data.get("shipping_apartment", None)

        billing_street_name = request.data.get("billing_street_name", None)
        billing_street_number = request.data.get("billing_street_number", None)
        billing_floor = request.data.get("billing_floor", None)
        billing_apartment = request.data.get("billing_apartment", None)

        use_default_shipping = request.data.get("use_default_shipping", None)
        use_default_billing = request.data.get("use_default_billing", None)
        use_billing_same_shipping = request.data.get("use_billing_same_shipping", None)

        try:
            customer = Customer.objects.get(customer_cookie_id=customer_cookie_id)
            order_qs = Order.objects.filter(customer=customer, ordered=False)
            if order_qs.exists():
                order = order_qs[0]
            else:
                return Response({"message":"no order"},status=HTTP_200_OK)

            # use default_adresses if not create new address obj and make it default_adress
            if use_default_shipping:
                order.shipping_address = customer.shipping_address
                if use_billing_same_shipping:
                    order.billing_address = customer.shipping_address
                else:
                    if use_default_billing:
                        order.billing_address = customer.billing_address
                    else:
                        billing_address = Address.objects.create(
                            street_name=billing_street_name,
                            street_number=billing_street_number,
                            floor=billing_floor,
                            apartment=billing_apartment,
                        )
                        billing_address.save()
                        order.billing_address = billing_address
                        customer.billing_address = billing_address
            else:
                shipping_address = Address.objects.create(
                    street_name=shipping_street_name,
                    street_number=shipping_street_number,
                    floor=shipping_floor,
                    apartment=shipping_apartment,
                )
                shipping_address.save()
                order.shipping_address = shipping_address
                customer.shipping_address = shipping_address
                if use_billing_same_shipping:
                    order.billing_address = shipping_address
                    customer.billing_address = shipping_address
                else:
                    if use_default_billing:
                        order.billing_address = customer.billing_address
                    else:
                        billing_address = Address.objects.create(
                            street_name=billing_street_name,
                            street_number=billing_street_number,
                            floor=billing_floor,
                            apartment=billing_apartment,
                        )
                        billing_address.save()
                        order.billing_address = billing_address
                        customer.billing_address = billing_address

            order.save()

            customer.name = name
            customer.last_name = last_name
            customer.phone_number = phone
            customer.email = email
            customer.save()

            return Response({"message":"ok"},status=HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                status=HTTP_400_BAD_REQUEST
            )


class SubmitPaymentAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        # info fetched from front-end for payment
        customer_cookie_id = request.data.get('customer_cookie_id', None)
        order_id = request.data.get("order_id", None)
        amount = request.data.get("amount", None)
        token = request.data.get("token", None)
        installments = request.data.get("installments", None)
        payment_method_id = request.data.get("payment_method_id", None)

        # check if order and customer exists
        try:
            customer = Customer.objects.get(customer_cookie_id=customer_cookie_id)
            order = Order.objects.get(id=order_id)
        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)

        # create payment
        charge = mp.post("/v1/payments",{
            "transaction_amount": round(amount,2),
            "payment_method_id": payment_method_id,
            "token": token,
            "installments": installments,
            "payer": {
                "email": "test_user_43865662@testuser.com" # e-mail de prueba
            }
        })

        print(charge)

        # manage responses
        if charge['response']['status'] == 'approved':
            payment = Payment.objects.create(
                order=order,
                customer=customer,
                approved=True,
                amount=amount,
                installments=charge['response']['installments'],
                installment_amount=charge['response']['transaction_details']['installment_amount'],
                total_amount=charge['response']['transaction_details']['total_paid_amount'],
            )

            order.ordered = True
            for order_item in order.order_items.all():
                order_item.ordered = True
                order_item.save()
            order.save()

            return Response(
                {"message":"ok"},
                status=HTTP_200_OK
            )
        elif charge['response']['status'] == 'in_process':
            payment = Payment.objects.create(
                order=order,
                customer=customer,
                pending=True,
                amount=amount,
                installments=charge['response']['installments'],
                installment_amount=charge['response']['transaction_details']['installment_amount'],
                total_amount=charge['response']['transaction_details']['total_paid_amount'],
            )

            order.ordered = True
            for order_item in order.order_items.all():
                order_item.ordered = True
                order_item.save()
            order.save()

            return Response(
                {"message":"pending"},
                status=HTTP_200_OK
            )
        elif charge['response']['status'] == 'rejected':
            if(charge['response']['status_detail'] == 'cc_rejected_bad_filled_card_number'):
                return Response(
                    {"message":"bad_filled_card_number"},status=HTTP_200_OK
                )
            elif(charge['response']['status_detail'] == 'cc_rejected_bad_filled_date'):
                return Response(
                    {"message":"bad_filled_date"},status=HTTP_200_OK
                )
            elif(charge['response']['status_detail'] == 'cc_rejected_bad_filled_other'):
                return Response(
                    {"message":"bad_filled_other"},status=HTTP_200_OK
                )
            elif(charge['response']['status_detail'] == 'cc_rejected_bad_filled_security_code'):
                return Response(
                    {"message":"bad_filled_security_code"},status=HTTP_200_OK
                )
            elif(charge['response']['status_detail'] == 'cc_rejected_blacklist'):
                return Response(
                    {"message":"blacklist"},status=HTTP_200_OK
                )
            elif(charge['response']['status_detail'] == 'cc_rejected_call_for_authorize'):
                return Response(
                    {"message":"call_for_authorize"},status=HTTP_200_OK
                )
            elif(charge['response']['status_detail'] == 'cc_rejected_card_disabled'):
                return Response(
                    {"message":"card_disabled"},status=HTTP_200_OK
                )
            elif(charge['response']['status_detail'] == 'cc_rejected_card_error'):
                return Response(
                    {"message":"card_error"},status=HTTP_200_OK
                )
            elif(charge['response']['status_detail'] == 'cc_rejected_duplicated_payment'):
                return Response(
                    {"message":"duplicated_payment"},status=HTTP_200_OK
                )
            elif(charge['response']['status_detail'] == 'cc_rejected_high_risk'):
                return Response(
                    {"message":"high_risk"},status=HTTP_200_OK
                )
            elif(charge['response']['status_detail'] == 'cc_rejected_insufficient_amount'):
                return Response(
                    {"message":"insufficient_amount"},status=HTTP_200_OK
                )
            elif(charge['response']['status_detail'] == 'cc_rejected_invalid_installments'):
                return Response(
                    {"message":"invalid_installments"},status=HTTP_200_OK
                )
            elif(charge['response']['status_detail'] == 'cc_rejected_max_attempts'):
                return Response(
                    {"message":"max_attempts"},status=HTTP_200_OK
                )
            elif(charge['response']['status_detail'] == 'cc_rejected_other_reason'):
                return Response(
                    {"message":"other_reason"},status=HTTP_200_OK
                )
            else:
                return Response(
                    {"message":"rejected"},status=HTTP_200_OK
                )
        else:
            return Response(status=HTTP_400_BAD_REQUEST)


class AddCouponOrderAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        order_id = request.data.get("order_id", None)
        code = request.data.get("code", None)

        try:
            order = Order.objects.get(id=order_id)
            coupon = CouponOrder.objects.get(code=code)

            order.coupon = coupon
            order.save()

            return Response({"message":"ok"}, status=HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=HTTP_400_BAD_REQUEST)
