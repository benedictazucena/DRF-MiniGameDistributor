from django.urls import path
from .views import UserAPIView

app_name = 'accounts'

urlpatterns = [
    path('users/', UserAPIView.as_view(), name='user-list-create'),
]
