from __future__ import unicode_literals
import os, sys, shutil
import optparse

from django.core.management.base import BaseCommand
from image_match_app.models import Image, QueryImage
from django.conf import settings as djsettings
import image_match_app.search as search

Option = optparse.make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        Option('--clear', action='store_const', const='clear', dest='action'),
        Option('--test', action='store_const', const='test', dest='action'),
    )

    def handle(self, *args, **options):
        action = options['action']
        if action == 'clear':
            QueryImage.clear()
        elif action == 'test':
            raise NotImplementedError
