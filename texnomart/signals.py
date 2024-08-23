import json
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from config.settings import BASE_DIR
from .models import Category, Product, Comment
import os
def send_notification_email(instance, created, **kwargs):
    action = 'created' if created else 'updated'
    subject = f'{instance.__class__.__name__} {action}'
    message = f'{instance.__class__.__name__} with ID {instance.id} has been {action}.'
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ['javlonbekalmamatov6@gmail.com'],  # Replace with the recipient's email
    )

def save_deleted_instance_to_json(instance):
    file_path = os.path.join(BASE_DIR,  'deleted_instances.json')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    data = {
        'model': instance.__class__.__name__,
        'id': instance.id,
    }

    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)



@receiver(post_save, sender=Category)
def category_post_save(sender, instance, created, **kwargs):
    send_notification_email(instance, created, **kwargs)

@receiver(post_delete, sender=Category)
def category_post_delete(sender, instance, **kwargs):
    send_notification_email(instance, created=False, **kwargs)
    save_deleted_instance_to_json(instance)

@receiver(post_save, sender=Product)
def product_post_save(sender, instance, created, **kwargs):
    send_notification_email(instance, created, **kwargs)

@receiver(post_delete, sender=Product)
def product_post_delete(sender, instance, **kwargs):
    send_notification_email(instance, created=False, **kwargs)
    save_deleted_instance_to_json(instance)

@receiver(post_save, sender=Comment)
def comment_post_save(sender, instance, created, **kwargs):
    send_notification_email(instance, created, **kwargs)

@receiver(post_delete, sender=Comment)
def comment_post_delete(sender, instance, **kwargs):
    send_notification_email(instance, created=False, **kwargs)
    save_deleted_instance_to_json(instance)
