import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servicehub.settings')
django.setup()

from django.template.loader import render_to_string

try:
    print("Attempting to render providers.html...")
    # Empty context usually breaks URLs if they expect arguments, 
    # but TemplateSyntaxError happens during compilation before render.
    # We will just compile it.
    from django.template.loader import get_template
    template = get_template('providers.html')
    print("SUCCESS: Template compiled successfully.")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
