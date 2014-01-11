from __future__ import unicode_literals
import optparse

from django.core.management.base import BaseCommand
from image_match_app.models import QueryImage
import image_match_app.search as search

Option = optparse.make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        Option('--clear', action='store_const', const='clear', dest='action'),
        Option('--test', action='store_const', const='test', dest='action'),
        Option('--rank_all', action='store_const', const='rank_all', dest='action'),
    )

    def handle(self, *args, **options):
        action = options['action']
        if action == 'clear':
            QueryImage.clear()
        elif action == 'test':
            raise NotImplementedError
        elif action == 'rank_all':
            saveTo = args[0]
            search.get_all_ranking(saveTo)
