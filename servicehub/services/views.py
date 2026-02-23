from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, ProviderProfile, Booking
from django.contrib import messages
from .forms import EmailForm
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})


def providers_by_category(request, category_id):
    providers = ProviderProfile.objects.filter(category_id=category_id)
    return render(request, 'providers.html', {'providers': providers})


@login_required
def user_dashboard(request):

    #Role protection
    if request.user.role != 'customer':
        return redirect('home')

    bookings = Booking.objects.filter(user=request.user)

    return render(request, 'dashboard.html', {
        'bookings': bookings
    })



@login_required
def provider_dashboard(request):

    #Role protection
    if request.user.role != 'provider':
        return redirect('home')

    try:
        provider = ProviderProfile.objects.get(user=request.user)
    except ProviderProfile.DoesNotExist:
        return redirect('home')

    bookings = Booking.objects.filter(service_provider=provider)

    return render(request, 'provider_dashboard.html', {
        'bookings': bookings
    })


@login_required
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.service_provider.user == request.user:
        booking.status = 'Accepted'
        booking.save()

    return redirect('provider_dashboard')


@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.service_provider.user == request.user:
        booking.status = 'Rejected'
        booking.save()

    return redirect('provider_dashboard')


@login_required
def book_provider(request, provider_id):

    # 🔒 Only customers can book
    if request.user.role != 'customer':
        return redirect('home')

    provider = get_object_or_404(ProviderProfile, id=provider_id)

    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        address = request.POST.get('address')

        Booking.objects.create(
            user=request.user,
            service_provider=provider,
            date=date,
            time=time,
            address=address,
            status='Pending'
        )

        messages.success(request, "Booking confirmed!")
        return redirect('user_dashboard')

    return render(request, 'book_provider.html', {
        'provider': provider
    })

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.user == request.user:
        booking.status = 'Cancelled'
        booking.save()
        messages.success(request, "Booking cancelled successfully!")

    return redirect('user_dashboard')

@login_required
def send_email_view(request):

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            sender = form.cleaned_data['sender']
            receiver = form.cleaned_data['receiver']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            send_mail(
                subject,
                message,
                sender,
                [receiver],
                fail_silently=False,
            )

            messages.success(request, "Email sent successfully!")
            return redirect('home')
    else:
        form = EmailForm()

    return render(request, 'send_email.html', {'form': form})