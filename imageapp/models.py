from django.contrib.auth.models import User
from django.db import models
from django_resized import ResizedImageField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, blank=True)
    original_image = models.ImageField(upload_to='original/', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'png'])])
    small_image = models.ImageField(upload_to='small/', editable=False, blank=True, default='')
    medium_image = models.ImageField(upload_to='medium/', editable=False, blank=True, default='')
    upload_date = models.DateTimeField(auto_now_add=True)
    original_url = models.TextField(null=True, blank=True, editable=False, default='')
    small_url = models.TextField(null=True, blank=True, editable=False, default='')
    medium_url = models.TextField(null=True, blank=True, editable=False, default='')
    time_url = models.TextField(null=True, blank=True, editable=False, default='')
    active_time = models.IntegerField(validators=[MinValueValidator(300), MaxValueValidator(30000)], null=True, blank=True)

    def __str__(self):
        return f"Image by {self.user}"
