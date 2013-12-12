from django.db import models
import os, sys

# Create your models here.
class Image(models.Model):
    path = models.FilePathField(max_length=200)
    hash = models.CharField(max_length=500)

    def delete(self):
        try:
            os.remove(self.path)
        except OSError as e:
            print >> sys.stderr, e
        super(Image, self).delete()

    def url(self):
        return '/image/%d' % (self.id,)

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
        empty = True
        for image in QueryImage.objects.all():
            image.delete()
            empty = False
        # if not empty:
        #     base = djsettings.QUERY_DIR
        #     for dir in os.listdir(base):
        #         os.rmdir(os.path.join(base, dir))
