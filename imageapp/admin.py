from django.contrib import admin
from .models import Image
from django.forms import forms


class ImageModelAdmin(admin.ModelAdmin):
    fields = ['original_image', 'active_time']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def change_view(self, request, object_id, form_url='', extra_context=None):
        return super().change_view(request, object_id, form_url=form_url, extra_context=extra_context)

    def save_form(self, request, form, change):
        return super().save_form(request, form, change)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)

admin.site.register(Image, ImageModelAdmin)




