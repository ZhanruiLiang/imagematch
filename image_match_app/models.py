import os
import sys

from django.db import models

# Create your models here.
class Image(models.Model):
    path = models.FilePathField(max_length=200)
    group = models.IntegerField()
    origin_id = models.IntegerField()

    def delete(self):
        try:
            os.remove(self.path)
        except OSError as e:
            print >> sys.stderr, e
        super(Image, self).delete()

class QueryImage(models.Model):
    path = models.FileField(
        upload_to='images/%d',
        max_length=200,
    )
    time = models.DateTimeField(auto_now_add=True)

    def delete(self):
        self.path.delete()
        super(QueryImage, self).delete()

    @staticmethod
    def clear():
        for image in QueryImage.objects.all():
            image.delete()
