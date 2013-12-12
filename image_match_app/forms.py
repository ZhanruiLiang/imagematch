from __future__ import unicode_literals
from django.db import models
from django import forms
import settings
import models

MAX_SIZE = settings.MAX_SIZE_PER_UPLOAD

def validate_size(self):
    if MAX_SIZE > 0 and self.size > MAX_SIZE:
        raise ValidationError(
            'Size limit exceeded, max: %(max).2f MB, yours: %(yours).2f MB.',
            params={
                'max': MAX_SIZE / float(2**20),
                'yours': self.size / float(2**20),
            })

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = models.QueryImage
        exclude = ('time', )
    path = forms.FileField(
            label='Upload an image',
            help_text = 'maxsize {:.2f} MB'.format(MAX_SIZE / float(2**20)),
            validators=[validate_size]
        )
