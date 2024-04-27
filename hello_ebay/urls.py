"""
URL configuration for hello_ebay project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import sales_report_view, delivery_status_view, generate_report_view
from .views import (UserDetailView, UserCreateView, UserUpdateView, UserDeleteView, UserListView,
                    ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, AddressListView, CategoryListView, ProductListView, 
    PhotoListView, AuctionListView, BidListView, OrderListView, 
    PaymentMethodListView, ReviewListView, PromotionListView, 
    DeliveryListView, ReportListView)

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path("admin/", admin.site.urls),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('users/add/', UserCreateView.as_view(), name='user_add'),
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/add/', ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('report/sales/', sales_report_view, name='sales_report'),
    path('delivery/update-status/<int:delivery_id>/', delivery_status_view, name='update_delivery_status'),
    path('report/generate/', generate_report_view, name='generate_report'),
    path('addresses/', AddressListView.as_view(), name='address-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('photos/', PhotoListView.as_view(), name='photo-list'),
    path('auctions/', AuctionListView.as_view(), name='auction-list'),
    path('bids/', BidListView.as_view(), name='bid-list'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('payment-methods/', PaymentMethodListView.as_view(), name='payment-method-list'),
    path('reviews/', ReviewListView.as_view(), name='review-list'),
    path('promotions/', PromotionListView.as_view(), name='promotion-list'),
    path('deliveries/', DeliveryListView.as_view(), name='delivery-list'),
    path('reports/', ReportListView.as_view(), name='report-list')
]
