from celery import shared_task
from .models import Delivery
import requests
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def generate_and_email_report():
    # Генерируем отчет здесь...
    report_data = "Отчетные данные"
    send_mail(
        'Отчет о продажах',
        report_data,
        settings.DEFAULT_FROM_EMAIL,
        ['admin@example.com'],
        fail_silently=False,
    )

@shared_task
def update_delivery_status(delivery_id):
    try:
        delivery = Delivery.objects.get(pk=delivery_id)
        # Внешний API, который возвращает статус доставки
        response = requests.get(
            f"{settings.EXTERNAL_DELIVERY_SERVICE_URL}/status",
            params={'order_id': delivery.order.id},
            headers={'Authorization': f"Token {settings.EXTERNAL_SERVICE_API_KEY}"}
        )

        if response.status_code == 200:
            status_data = response.json()
            delivery.status = status_data['status']
            delivery.save()
            # Можете добавить здесь дополнительную логику, например, уведомление пользователя
        else:
            # Логирование ошибки, если запрос не удался
            print(f"Ошибка при обновлении статуса доставки: {response.status_code}")
    except Delivery.DoesNotExist:
        # Логирование ошибки, если запись доставки не найдена
        print(f"Доставка с id {delivery_id} не найдена.")
    except requests.RequestException as e:
        # Логирование исключения при проблеме с запросом к внешнему API
        print(f"Ошибка при запросе к внешнему сервису доставки: {e}")
