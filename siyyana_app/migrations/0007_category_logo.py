# Generated by Django 5.0.7 on 2024-08-13 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siyyana_app', '0006_rename_services_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='logo',
            field=models.ImageField(default=1, upload_to='category'),
            preserve_default=False,
        ),
    ]
