from django.contrib import admin
from .models import User, Address, Category, Product, Photo, Auction, Bid, Order, PaymentMethod, Review, Promotion, Delivery

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active', 'is_admin']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'city', 'street', 'postal_code']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'status']

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['product', 'file_link', 'description']

@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ['product', 'starting_price', 'start_time', 'end_time']

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['auction', 'user', 'bid_amount', 'bid_time']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_date', 'delivery_status']

@admin.register(PaymentMethod)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'card_type', 'card_number', 'expiration_date', 'cvv']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'date']

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['description', 'start_time', 'end_time', 'discount']

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'address']