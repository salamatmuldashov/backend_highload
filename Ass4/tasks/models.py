from django.db import models
from django.core.exceptions import ValidationError


class Website(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    url = models.URLField()

    def __str__(self):
        return self.name



def validate_file_type(file):
    allowed_extensions = ['.csv']
    extension = file.name.split('.')[-1]
    if extension not in allowed_extensions:
        raise ValidationError(f"File type not allowed. Only {', '.join(allowed_extensions)} files are allowed.")

class Dataset(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    file = models.FileField(upload_to='datasets/', validators=[validate_file_type])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    progress = models.IntegerField(default=0) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Dataset {self.id} - {self.status}"