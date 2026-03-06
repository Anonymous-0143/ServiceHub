from django.urls import path
from .views import home, providers_by_category
from .import views

urlpatterns = [
    path('', home, name='home'),
    path('providers/<int:category_id>/', providers_by_category, name='providers_by_category'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('provider/dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('booking/<int:booking_id>/accept/', views.accept_booking, name='accept_booking'),
    path('booking/<int:booking_id>/reject/', views.reject_booking, name='reject_booking'),
    path('book/<int:provider_id>/', views.book_provider, name='book_provider'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('review/<int:booking_id>/', views.submit_review, name='submit_review'),
    path('provider/<int:provider_id>/reviews/', views.provider_reviews, name='provider_reviews'),
    path('api/geocode/', views.geocode_api, name='geocode_api'),
    path('payment/success/', views.payment_success, name='payment_success'),
]


