from __future__ import unicode_literals
import os, sys, shutil
import optparse

import image_match_app.search as search
from django.core.management.base import BaseCommand

Option = optparse.make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            Option('--debug', action='store_true', dest='debug'),
        )

    def handle(self, *args, **options):
        if options['debug']:
            search.debug_get_likelyhood(args[0], args[1])
