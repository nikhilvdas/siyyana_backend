from django.contrib import admin
from django.apps import apps
# Register your models here.
myadmin_models = apps.get_app_config('siyyana_app').get_models()

# Register all models in the Django admin
for model in myadmin_models:
    admin.site.register(model)