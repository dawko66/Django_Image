from django.contrib import admin
from .models import Image
import PIL
import datetime
from io import BytesIO
from django.conf import settings


class ImageModelAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is not None:
            field = form.base_fields['original_image']
            field.widget = field.hidden_widget()

            field = form.base_fields['active_time']
            field.widget = field.hidden_widget()

        return form

    def save_model(self, request, obj, form, change):
        obj.user = request.user

        image_data = obj.original_image
        name = image_data.name

        def resize(img, height):
            extension = str.upper(img.name.split('.')[-1])
            extension = 'JPEG' if extension == 'JPG' else extension

            image = PIL.Image.open(img)
            width_percent = (height / image.width)
            new_width = int((float(image.height) * float(width_percent)))
            image.thumbnail((new_width, height))
            image_data = BytesIO()
            image.save(image_data, format=extension)
            return image_data

        base_url = settings.SERVER_URL + 'imageapp/encrypted_image/'

        obj.small_image.save(name, resize(image_data, 200))
        obj.small_url = base_url + obj.small_image.name.replace('small/', 'small', 1)

        obj.medium_image.save(name, resize(image_data, 400))
        obj.medium_url = base_url + obj.medium_image.name.replace('medium/', 'medium', 1)

        obj.original_image.save(name, image_data)
        obj.original_url = base_url + obj.original_image.name.replace('original/', 'original', 1)

        if obj.active_time is not None:
            active_time = datetime.datetime.now() + datetime.timedelta(seconds=300)
            obj.time_url = base_url + str(active_time) + obj.original_image.name.replace('original/', 'original', 1)

        obj.save()
        return super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        return ['small_url', 'medium_url', 'original_url', 'time_url']

admin.site.register(Image, ImageModelAdmin)
