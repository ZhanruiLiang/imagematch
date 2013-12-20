import sys, os, shutil
import pHash
from models import Image, QueryImage
from django.conf import settings as djsettings
import datetime

def search(image, number=100):
    """
    image: models.QueryImage object
    return: a list of matched results, with type models.Image .
    """
    path = image.path.path
    hash = pHash.imagehash(path)
    a = [(pHash.hamming_distance(hash, int(img.hash)), img) 
            for img in Image.objects.all()]
    a.sort(key=lambda (h, img): h)
    results = a[:number]
    return results

def import_image(src_path, dst_path):
    # copy to storePath
    shutil.copy(src_path, dst_path)
    image = Image(
            path=dst_path,
            hash=str(pHash.imagehash(dst_path)),
        )
    image.save()
    return image
