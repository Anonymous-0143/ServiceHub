from django.urls import path
from .views import book_provider

urlpatterns = [
    path('book/<int:provider_id>/', book_provider, name='book_provider'),
]