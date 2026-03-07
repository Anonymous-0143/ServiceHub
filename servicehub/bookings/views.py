from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking, Message
from services.models import ProviderProfile
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def chat_room(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Ensure the user is either the customer or the provider
    if request.user != booking.user and request.user != booking.service_provider.user:
        return redirect('home')

    messages = booking.messages.all()

    context = {
        'booking': booking,
        'messages': messages,
    }
    return render(request, 'bookings/chat.html', context)
