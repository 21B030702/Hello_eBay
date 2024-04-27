from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import User, Product
from django.views.generic import ListView, DetailView
from .tasks import generate_and_email_report, update_delivery_status
from django.http import JsonResponse
from .utils import get_category_sales
from django.shortcuts import render
from rest_framework import generics
from .models import User, Address, Category, Product, Photo, Auction, Bid, Order, PaymentMethod, Review, Promotion, Delivery, Report
from .serializers import UserSerializer, AddressSerializer, CategorySerializer, ProductSerializer, PhotoSerializer, AuctionSerializer, BidSerializer, OrderSerializer, PaymentMethodSerializer, ReviewSerializer, PromotionSerializer, DeliverySerializer, ReportSerializer
from rest_framework.generics import ListAPIView

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/user_detail.html'

class UserCreateView(CreateView):
    model = User
    fields = ['name', 'email', 'password', 'status']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

class UserUpdateView(UpdateView):
    model = User
    fields = ['name', 'email', 'password', 'status']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user_list')

class UserDeleteView(DeleteView):
    model = User
    context_object_name = 'user'
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

# Продукты
class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/product_list.html'

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/product_detail.html'

class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'description', 'category', 'price', 'status', 'keywords']
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'description', 'category', 'price', 'status', 'keywords']
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

def sales_report_view(request):
    # Запускаем задачу Celery и отправляем отчет на email
    generate_and_email_report.delay()
    return JsonResponse({"status": "Отчет сгенерирован и отправлен."})

def category_sales_view(request):
    data = get_category_sales()
    return JsonResponse(data, safe=False)

def delivery_status_view(request, delivery_id):
    # Запускаем задачу Celery для обновления статуса доставки
    update_delivery_status.delay(delivery_id)
    return JsonResponse({"status": "Обновление статуса доставки инициировано."})

def generate_report_view(request):
    report_data = get_category_sales()
    return render(request, 'reports/generate_report.html', {'report_data': report_data})

class AddressListView(generics.ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class PhotoListView(generics.ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class AuctionListView(generics.ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer

class BidListView(generics.ListAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class PaymentMethodListView(generics.ListAPIView):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class PromotionListView(generics.ListAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

class DeliveryListView(generics.ListAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

class ReportListView(ListAPIView):
      queryset = Report.objects.all()
      serializer_class = ReportSerializer