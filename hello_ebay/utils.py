from django.core.cache import cache
from .models import Product
from django.db.models import Sum, Count

def generate_sales_report():
    # Определение функции для генерации отчета о продажах...
    category_sales = (
        Product.objects
        .values('category__name')
        .annotate(total_sales=Sum('order__total_amount'), total_orders=Count('order'))
        .order_by('-total_sales')
    )
    return category_sales

def get_category_sales():
    if 'category_sales' in cache:
        return cache.get('category_sales')
    else:
        result = generate_sales_report()
        cache.set('category_sales', result, timeout=3600)  # Кешируйте результат на час
        return result