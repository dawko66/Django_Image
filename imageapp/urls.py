from django.urls import path, include
from rest_framework import routers
from .views import ImageViewSet, EncryptedImage, ImageListView

router = routers.DefaultRouter()
router.register(r'images-upload', ImageViewSet, basename='images-upload')
router.register(r'images-list', ImageListView, basename='images-list')

urlpatterns = [
    path('api/', include(router.urls)),
    path('encrypted_image/<str:encrypted_link>/', EncryptedImage.as_view(), name='encrypted_image'),
]
