from django.db import migrations


def seed_categories(apps, schema_editor):
    Category = apps.get_model('services', 'Category')
    categories = [
        {'name': 'Plumbing', 'slug': 'plumbing', 'description': 'Water pipes, leaks, installations and repairs.'},
        {'name': 'Electrical', 'slug': 'electrical', 'description': 'Wiring, fuse boxes, lighting and electrical repairs.'},
        {'name': 'Cleaning', 'slug': 'cleaning', 'description': 'Home and office deep cleaning services.'},
        {'name': 'Carpentry', 'slug': 'carpentry', 'description': 'Furniture assembly, woodwork and repairs.'},
        {'name': 'Painting', 'slug': 'painting', 'description': 'Interior and exterior painting services.'},
        {'name': 'AC Repair', 'slug': 'ac-repair', 'description': 'Air conditioner installation, service and repair.'},
        {'name': 'Appliance Repair', 'slug': 'appliance-repair', 'description': 'Washing machine, fridge and home appliance repairs.'},
        {'name': 'Pest Control', 'slug': 'pest-control', 'description': 'Cockroach, termite, rodent and pest elimination.'},
        {'name': 'Gardening', 'slug': 'gardening', 'description': 'Lawn care, plant maintenance and landscaping.'},
        {'name': 'Home Shifting', 'slug': 'home-shifting', 'description': 'Packing, moving and unpacking services.'},
    ]
    for cat in categories:
        Category.objects.get_or_create(slug=cat['slug'], defaults=cat)


def reverse_categories(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_booking_payment_status_booking_razorpay_order_id_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_categories, reverse_categories),
    ]
