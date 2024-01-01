from django.urls import path
from .views import (AuthFaceView)

urlpatterns = [
    path('authface/', AuthFaceView.as_view(), name='auth_face')
]