from django.urls import path
from . api import (
    NewCustomerAPIView,

    HomeItemsAPIView,
    AllItemsAPIView,
    CategoriesAPIView,
    ItemVariationsAPIView,

    CustomerOrderAPIView,
    AddItemToCartAPIView,
    DeleteItemFromCartAPIView,
    AddOneItemAPIView,
    DeleteOneItemAPIView,

    SubmitCheckoutAPIView,
    CustomerInfoAPIView,
    SubmitPaymentAPIView,

    AddCouponOrderAPIView,
)

urlpatterns = [
    path('new-customer/', NewCustomerAPIView.as_view(), name="new-customer"),

    path('home-items/', HomeItemsAPIView.as_view(), name="home-items"),
    path('all-items/', AllItemsAPIView.as_view(), name="all-items"),
    path('categories/', CategoriesAPIView.as_view(), name="categories"),
    path('item-variations/', ItemVariationsAPIView.as_view(), name="item-variations"),

    path('customer-order/', CustomerOrderAPIView.as_view(), name="customer-order"),
    path('add-item-to-cart/', AddItemToCartAPIView.as_view(), name="add-item-to-cart"),
    path('delete-item-from-cart/', DeleteItemFromCartAPIView.as_view(), name="delete-item-from-cart"),
    path('add-one-item/', AddOneItemAPIView.as_view(), name="add-one-item"),
    path('delete-one-item/', DeleteOneItemAPIView.as_view(), name="delete-one-item"),

    path('customer-info/', CustomerInfoAPIView.as_view(), name="customer-info"),
    path('submit-checkout/', SubmitCheckoutAPIView.as_view(), name="submit-checkout"),
    path('submit-payment/', SubmitPaymentAPIView.as_view(), name="submit-payment"),

    path('add-coupon-order/', AddCouponOrderAPIView.as_view(), name="add-coupon-order"),
]
