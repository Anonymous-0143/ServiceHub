from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking
from services.models import ProviderProfile
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def book_provider(request, provider_id):
    provider = get_object_or_404(User, id=provider_id)
    
    if request.method == 'POST':
       

        date = request.POST.get('date')
        time = request.POST.get('time')
        address = request.POST.get('address')

        booking = Booking.objects.create(
            customer=request.user,
            provider=provider,
            date=date,
            time=time,
            address=address
        )

        return redirect('dashboard')
    return render(request, 'bookings/book_provider.html', {'form': form, 'provider': provider})

# Create your views here.
