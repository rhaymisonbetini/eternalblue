from django.urls import path
from .views import (AuthFaceView, SQLGeneratorView)

urlpatterns = [
    path('authface/', AuthFaceView.as_view(), name='auth_face'),
    path('sqlgenerator/', SQLGeneratorView.as_view(), name='sql_generator')
]
