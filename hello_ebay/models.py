from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password=password, **extra_fields)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField('last login', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
class Address(models.Model):
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    keywords = models.TextField()

    def __str__(self):
        return self.name

class Photo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file_link = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.file_link

class Auction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Auction for {self.product.name}"

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user.name} - {self.bid_amount}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_status = models.CharField(max_length=50)

    def __str__(self):
        return f"Order {self.id} by {self.user.name}"

class PaymentMethod(models.Model):
    user = models.ForeignKey(User, related_name='payment_methods', on_delete=models.CASCADE)
    card_type = models.CharField(max_length=50)
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.card_type} ending in {self.card_number[-4:]}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return f"Review by {self.user.name}"

class Promotion(models.Model):
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    discount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.description

class DeliveryStatus(models.TextChoices):
        PROCESSING = 'processing', 'Processing'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        RETURNED = 'returned', 'Returned'
        CANCELLED = 'cancelled', 'Cancelled'

class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    status = models.CharField(max_length=50, choices=DeliveryStatus.choices)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    

class Report(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    data = models.JSONField() 