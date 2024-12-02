from datetime import timezone
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from .models import Dataset


@shared_task(bind=True, max_retries=3)
def send_email_task(self, recipient, subject, body):
    try:
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,
            [recipient],
        )
        return f'Email sent successfully to {recipient}'
    except Exception as exc:
        raise self.retry(exc=exc)

import csv



@shared_task
def process_dataset(dataset_id):
    dataset = Dataset.objects.get(id=dataset_id)
    dataset.status = 'processing'
    dataset.progress = 0  

    dataset.save()

    try:
        data = []
        total_rows = sum(1 for _ in dataset.file.open('r'))  # Total rows in the CSV
        processed_rows = 0

        with dataset.file.open('r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'Period' not in row or 'Magnitude' not in row:
                    raise ValidationError(f"Missing required columns in row: {row}")
            

                data.append(row)
                processed_rows += 1
                dataset.progress = int((processed_rows / total_rows) * 100)
                dataset.save()


        dataset.processed_data = data
        dataset.status = 'completed'
        dataset.progress = 100
        dataset.save()

    except ValidationError as e:
        dataset.status = 'failed'
        dataset.save()
        raise e
