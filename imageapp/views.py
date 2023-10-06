from .models import Image
from rest_framework import viewsets
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ImageSerializer, ImageListSerializer
from django.http import HttpResponse
import PIL
import datetime


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        links = []
        if serializer.instance.small_url:
            links.append({'name': 'Image 200px', 'url': serializer.instance.small_url})
        if serializer.instance.medium_url:
            links.append({'name': 'Image 400px', 'url': serializer.instance.medium_url})
        if serializer.instance.original_url:
            links.append({'name': 'Image original', 'url': serializer.instance.original_url})
        if serializer.instance.time_url:
            links.append({'name': 'Time image', 'url': serializer.instance.time_url})

        link_list = '<ul>'
        for link in links:
            link_list += f'<li><a href="{link["url"]}">{link["name"]}</a></li>'
        link_list += '</ul>'

        response = HttpResponse(link_list, content_type='text/html')

        return response

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        if serializer.validated_data.get('active_time') is None:
            serializer.validated_data['active_time'] = 0
        serializer.save()

    def get_queryset(self):
        user = self.request.user
        image = Image.objects.filter(user=user)
        return image

class ImageListView(viewsets.ReadOnlyModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageListSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Image.objects.filter(user=request.user)
        serializer = ImageListSerializer(queryset, many=True)
        return Response(serializer.data)

class EncryptedImage(APIView):
    queryset = Image.objects.all()

    def get_image(self, image_path):
        try:
            try:
                active_time_str = image_path.split('original')[0]
                active_time = datetime.datetime.strptime(active_time_str, "%Y-%m-%d %H:%M:%S.%f")
                image_path = image_path[len(str(active_time_str)):]
            except:
                active_time = None

            if not active_time or datetime.datetime.now() < active_time:
                media_folder = settings.BASE_DIR / settings.MEDIA_FOLDER
                if image_path[:5] == 'small':
                    image_path = media_folder / image_path[:5] / image_path[5:]
                elif image_path[:6] == 'medium':
                    image_path = media_folder / image_path[:6] / image_path[6:]
                elif image_path[:8] == 'original':  # len('original')
                    image_path = media_folder / image_path[:8] / image_path[8:]

                image = PIL.Image.open(image_path)
                return image
            else:
                return None

        except FileNotFoundError:
            return None

    def finalize_response(self, request, response, *args, **kwargs):
        image_path = self.request.parser_context.get('kwargs').get('encrypted_link')
        image = self.get_image(image_path)

        if image:
            extension = str.upper(image_path.split('.')[-1])
            extension = 'JPEG' if extension == 'JPG' else extension

            response = HttpResponse(content_type="image/jpeg")
            image.save(response, extension)
            return response
        else:
            return HttpResponse(status=404)
