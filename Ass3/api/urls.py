from django.urls import path
from .views import DataReadView, DataWriteView

urlpatterns = [
    path('data/<str:key>/', DataReadView.as_view(), name='data_read_view'),  # For GET
    path('data/', DataWriteView.as_view(), name='data_write_view'),  # For POST
]
