from rest_framework import serializers
from .models import Website, Dataset

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ['name', 'age', 'url']



class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'file', 'status', 'created_at', 'updated_at', 'processed_data']
        read_only_fields = ['status', 'created_at', 'updated_at', 'processed_data']
