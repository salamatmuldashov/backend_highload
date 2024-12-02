from django.urls import path
from .views import send_email_view, register, login, verify_otp, home, WebsiteListCreate, WebsiteDetail, DatasetUploadView, DatasetListView, DatasetProgressView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('send-email/', send_email_view, name='send_email'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('home/', home, name='home'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('websites/', WebsiteListCreate.as_view(), name='website-list'),
    path('websites/<int:pk>/', WebsiteDetail.as_view(), name='website-detail'),
    path('upload/', DatasetUploadView.as_view(), name='dataset-upload'),
    path('list_csv/', DatasetListView.as_view(), name='dataset-list'),
    path('progress/<int:pk>/', DatasetProgressView.as_view(), name='dataset_progress'),

]