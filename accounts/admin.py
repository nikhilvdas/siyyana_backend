from django.contrib import admin
from django.apps import apps

myadmin_models = apps.get_app_config('accounts').get_models()

for model in myadmin_models:
    admin.site.register(model)



