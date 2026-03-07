

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, ProviderProfile, Booking, Review
from django.contrib import messages
from .forms import FeedbackForm, ReviewForm
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg, Count, Sum


def home(request):
    categories = Category.objects.all()
    context = {'categories': categories}

    if request.user.is_authenticated and request.user.role == 'provider':
        try:
            provider = ProviderProfile.objects.get(user=request.user)
            
            # 1. Active Jobs (Pending or Accepted)
            active_jobs = Booking.objects.filter(service_provider=provider, status__in=['Pending', 'Accepted']).count()
            
            # 2. Total Earnings
            earnings_agg = Booking.objects.filter(service_provider=provider, payment_status='Paid').aggregate(total=Sum('total_amount'))
            total_earnings = earnings_agg['total'] or 0.00
            
            # 3. Average Rating
            stats = provider.reviews.aggregate(avg_rating=Avg('rating'))
            avg_rating = stats['avg_rating'] or 0.0
            
            # 4. Recent Activity (Last 5 bookings)
            recent_activity = Booking.objects.filter(service_provider=provider).order_by('-id')[:5]

            context.update({
                'active_jobs': active_jobs,
                'total_earnings': total_earnings,
                'avg_rating': round(avg_rating, 1),
                'recent_activity': recent_activity
            })
        except ProviderProfile.DoesNotExist:
            pass

    return render(request, 'home.html', context)


from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def providers_by_category(request, category_id):
    providers = ProviderProfile.objects.filter(category_id=category_id)
    
    location_query = request.GET.get('location', '')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if lat and lon:
        try:
            geolocator = Nominatim(user_agent="servicehub_app")
            # Reverse lookup the coordinates
            location_data = geolocator.reverse(f"{lat}, {lon}", exactly_one=True)
            if location_data and location_data.raw.get('address'):
                address = location_data.raw['address']
                # Try to get the city, town, or village name
                location_query = address.get('city') or address.get('town') or address.get('village') or ''
        except (GeocoderTimedOut, GeocoderServiceError):
            messages.error(request, "Could not determine location from GPS. Please try the manual search.")
            
    if location_query:
        providers = providers.filter(location__icontains=location_query)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_rating = request.GET.get('min_rating')
    sort_by = request.GET.get('sort_by')

    if min_price:
        providers = providers.filter(hourly_rate__gte=min_price)
    if max_price:
        providers = providers.filter(hourly_rate__lte=max_price)

    providers = providers.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews'),
    )

    if min_rating:
        providers = providers.filter(avg_rating__gte=min_rating)

    if sort_by == 'price_asc':
        providers = providers.order_by('hourly_rate')
    elif sort_by == 'price_desc':
        providers = providers.order_by('-hourly_rate')
    elif sort_by == 'rating_desc':
        providers = providers.order_by('-avg_rating')
    elif sort_by == 'experience_desc':
        providers = providers.order_by('-experience')

    return render(request, 'providers.html', {
        'providers': providers,
        'location_query': location_query,
        'min_price': min_price,
        'max_price': max_price,
        'min_rating': min_rating,
        'sort_by': sort_by
    })


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
    stats = provider.reviews.aggregate(avg_rating=Avg('rating'), review_count=Count('id'))

    return render(request, 'provider_dashboard.html', {
        'bookings': bookings,
        'avg_rating': stats['avg_rating'],
        'review_count': stats['review_count'],
    })


try:
    import razorpay
except ImportError:
    razorpay = None
from django.conf import settings

@login_required
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.service_provider.user == request.user:
        booking.status = 'Accepted'
        
        # Initialize Razorpay Client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        # Calculate total amount based on hourly rate (assuming 1 hour for MVP)
        amount_in_rupees = booking.service_provider.hourly_rate
        booking.total_amount = amount_in_rupees
        amount_in_paisa = int(amount_in_rupees * 100)
        
        # Create Razorpay Order
        data = { "amount": amount_in_paisa, "currency": "INR", "receipt": f"booking_{booking.id}" }
        try:
            payment = client.order.create(data=data)
            booking.razorpay_order_id = payment['id']
            booking.payment_status = 'Pending'
        except Exception as e:
            messages.error(request, f"Could not generate payment order: {e}")
            
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
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST, user=request.user)
        if form.is_valid():
            feedback_type = form.cleaned_data['feedback_type']
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['message']

            full_subject = f"[ServiceHub {feedback_type.upper()}] {subject}"
            full_message = (
                f"From: {request.user.get_full_name() or request.user.username} "
                f"({request.user.email})\n"
                f"Role: {request.user.role}\n"
                f"Type: {feedback_type}\n\n"
                f"{body}"
            )

            send_mail(
                full_subject,
                full_message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],  # sends to admin
                fail_silently=False,
            )

            messages.success(request, "Your feedback has been sent to the admin. Thank you!")
            return redirect('feedback')
    else:
        form = FeedbackForm(user=request.user)

    return render(request, 'feedback.html', {'form': form})


@login_required
def submit_review(request, booking_id):
    """Customer submits a review for a completed booking."""
    booking = get_object_or_404(Booking, id=booking_id)

    # Only the booking owner can review
    if booking.user != request.user:
        return redirect('user_dashboard')

    # Only accepted bookings can be reviewed
    if booking.status != 'Accepted':
        messages.error(request, "You can only review accepted bookings.")
        return redirect('user_dashboard')

    # Prevent duplicate reviews
    if hasattr(booking, 'review'):
        messages.info(request, "You have already reviewed this booking.")
        return redirect('user_dashboard')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(
                booking=booking,
                reviewer=request.user,
                provider=booking.service_provider,
                rating=int(form.cleaned_data['rating']),
                comment=form.cleaned_data['comment'],
            )
            messages.success(request, "Thank you for your review!")
            return redirect('user_dashboard')
    else:
        form = ReviewForm()

    return render(request, 'review_form.html', {
        'form': form,
        'booking': booking,
    })


def provider_reviews(request, provider_id):
    """Public page showing all reviews for a provider."""
    provider = get_object_or_404(ProviderProfile, id=provider_id)
    reviews = provider.reviews.select_related('reviewer').order_by('-created_at')
    stats = reviews.aggregate(avg_rating=Avg('rating'), review_count=Count('id'))

    return render(request, 'provider_reviews.html', {
        'provider': provider,
        'reviews': reviews,
        'avg_rating': stats['avg_rating'],
        'review_count': stats['review_count'],
    })

from django.http import JsonResponse

def geocode_api(request):
    """
    JSON API Endpoint that accepts ?lat=X&lon=Y and returns {"location": "City Name"}
    """
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    if not lat or not lon:
        return JsonResponse({'error': 'Missing lat or lon'}, status=400)

    try:
        geolocator = Nominatim(user_agent="servicehub_app_ajax")
        location_data = geolocator.reverse(f"{lat}, {lon}", exactly_one=True)
        
        if location_data and location_data.raw.get('address'):
            address = location_data.raw['address']
            city = address.get('city') or address.get('town') or address.get('village') or ''
            return JsonResponse({'location': city})
        
        return JsonResponse({'location': ''})
    
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        return JsonResponse({'error': str(e)}, status=500)

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

@csrf_exempt
def payment_success(request):
    """
    Razorpay calls this when a payment successfully completes.
    We must verify the signature cryptographically to prevent fraud.
    """
    if request.method == "POST":
        data = request.POST
        payment_id = data.get('razorpay_payment_id', '')
        order_id = data.get('razorpay_order_id', '')
        signature = data.get('razorpay_signature', '')
        
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        try:
            # Automatic signature verification
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })
            
            # Find the booking and mark it as Paid
            booking = Booking.objects.get(razorpay_order_id=order_id)
            booking.payment_status = 'Paid'
            booking.save()
            
            messages.success(request, f"Your payment of ₹{booking.total_amount} was successful!")
            return redirect('user_dashboard')
            
        except razorpay.errors.SignatureVerificationError:
            messages.error(request, "Payment signature verification failed. Possible fraud attempt.")
            return HttpResponseBadRequest("Signature Failed")
            
    return redirect('home')