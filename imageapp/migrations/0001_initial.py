# Generated by Django 4.2.5 on 2023-10-05 19:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_image', models.ImageField(upload_to='original/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png'])])),
                ('small_image', models.ImageField(blank=True, default='', editable=False, upload_to='small/')),
                ('medium_image', models.ImageField(blank=True, default='', editable=False, upload_to='medium/')),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('original_url', models.TextField(blank=True, default='', editable=False, null=True)),
                ('small_url', models.TextField(blank=True, default='', editable=False, null=True)),
                ('medium_url', models.TextField(blank=True, default='', editable=False, null=True)),
                ('time_url', models.TextField(blank=True, default='', editable=False, null=True)),
                ('active_time', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(300), django.core.validators.MaxValueValidator(30000)])),
                ('user', models.ForeignKey(blank=True, editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]