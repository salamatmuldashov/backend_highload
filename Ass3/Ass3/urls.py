from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path(r'^__debug__/', include('debug_toolbar.urls')),
    path('', include('django_prometheus.urls')),

]
