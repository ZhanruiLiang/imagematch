import pHash
from models import Image, QueryImage
from django.conf import settings as djsettings
import datetime

def search(image, number=10):
    """
    image: models.QueryImage object
    return: a list of matched results, with type models.Image .
    """
    # TODO
    results = Image.objects.all()[:5]
    return results
