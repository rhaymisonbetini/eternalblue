import base64
from django.core.files.base import ContentFile
from django.conf import settings
import os
import uuid


class Uploads:
    @staticmethod
    def save_image(image_data) -> str:
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        unique_filename = str(uuid.uuid4()) + '.' + ext
        data = ContentFile(base64.b64decode(imgstr), name=unique_filename)
        file_path = os.path.join(settings.MEDIA_ROOT, unique_filename)
        with open(file_path, 'wb') as f:
            f.write(data.read())

        return str(file_path)

    @staticmethod
    def remove_file(path: str):
        if os.path.exists(path):
            os.remove(path)
