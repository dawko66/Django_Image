from rest_framework import serializers
from .models import Image
import PIL
import datetime
from io import BytesIO
from django.conf import settings


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['original_image', 'upload_date', 'active_time']

    def get_fields(self):
        fields = super(ImageSerializer, self).get_fields()
        user = self.context['request'].user

        user_groups = user.groups.all()
        for group in user_groups:
            if group.name == 'Enterprise':
                pass
            elif group.name == 'Premium':
                del fields['active_time']
            elif group.name == 'Basic':
                del fields['active_time']

        return fields

    def create(self, validated_data):
        image_data = validated_data.pop('original_image')
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

        image_obj = Image(user=validated_data.get('user'))

        base_url = settings.SERVER_URL + 'imageapp/encrypted_image/'

        image_obj.small_image.save(name, resize(image_data, 200))
        image_obj.small_url = base_url + image_obj.small_image.name.replace('small/', 'small', 1)

        user_groups = validated_data['user'].groups.all()
        for group in user_groups:
            if group.name == 'Enterprise' or group.name == 'Premium':
                image_obj.medium_image.save(name, resize(image_data, 400))
                image_obj.medium_url = base_url + image_obj.medium_image.name.replace('medium/', 'medium', 1)

                image_obj.original_image.save(name, image_data)
                image_obj.original_url = base_url + image_obj.original_image.name.replace('original/', 'original', 1)

            if group.name == 'Enterprise' and validated_data['active_time'] > 0:
                image_obj.active_time = validated_data['active_time']
                active_time = datetime.datetime.now() + datetime.timedelta(seconds=300)

                image_obj.time_url = base_url + str(active_time) + image_obj.original_image.name.replace('original/', 'original', 1)

        image_obj.save()
        return image_obj

class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['small_url', 'medium_url', 'original_url', 'time_url']
