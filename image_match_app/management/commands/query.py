from __future__ import unicode_literals
import os, sys, shutil
import optparse

from django.core.management.base import BaseCommand
from image_match_app.models import Image, QueryImage
from django.conf import settings as djsettings

Option = optparse.make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            Option('--clear', action='store_true', dest='clear', default=False),
        )

    def handle(self, *args, **options):
        if options['clear']:
            QueryImage.clear()
