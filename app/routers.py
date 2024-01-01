from django.urls import path
from .views import (AuthFaceView, SQLGeneratorView, BodeView)

urlpatterns = [
    path('authface/', AuthFaceView.as_view(), name='auth_face'),
    path('sqlgenerator/', SQLGeneratorView.as_view(), name='sql_generator'),
    path('sqlbode/', BodeView.as_view(), name='sql_generator')
]
