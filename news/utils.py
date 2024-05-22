import requests
from django.core.files.base import ContentFile


def save_image_from_url(url, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        return ContentFile(response.content, name=file_name)
    return None
