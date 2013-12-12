from __future__ import unicode_literals
import os, sys, shutil
import optparse
import datetime

import image_match_app.search as search
from django.core.management.base import BaseCommand
from image_match_app.models import Image, QueryImage
from django.conf import settings as djsettings

Option = optparse.make_option

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            Option('-a', '--add', action='store_true', dest='add', default=False),
            Option('--clear', action='store_true', dest='clear', default=False),
            Option('-s', '--status', action='store_true', dest='status', default=False),
            Option('--prefix', 
                action='store', type='string', default='', dest='prefix'),
        )

    def handle(self, *args, **options):
        if options['clear']:
            assert not options['add']
            self.clear_images_db()

        if options['add']:
            prefix = options['prefix']
            for srcPath in args:
                self.import_to_images_db(srcPath, prefix)

        if options['status']:
            self.show_status()

    def show_status(self):
        num = Image.objects.count()
        self.stdout.write('totally %d images in database' % num)

    def clear_images_db(self):
        for image in Image.objects.all():
            image.delete()
        # storePath = djsettings.IMAGES_DIR
        # for dir in os.listdir(storePath):
        #     os.rmdir(os.path.join(storePath, dir))

    def import_to_images_db(self, dir_path, prefix):
        if not prefix:
            prefix = datetime.datetime.now().strftime('%m-%d-%h-%H:%M')
        storePath = os.path.join(djsettings.IMAGES_DIR, prefix)
        if not os.path.exists(storePath):
            os.mkdir(storePath)
        count = 0
        for fname in os.listdir(dir_path):
            srcPath = os.path.join(dir_path, fname)
            ext = os.path.splitext(fname)[1]
            if ext in ('.jpg', '.png'):
                # create new Image instance
                dstPath = os.path.join(storePath, '%s%s'%(count, ext))
                image = search.import_image(srcPath, dstPath)
                self.stdout.write('add [%s] as [%s].' % (srcPath, image.path))
                count += 1
            else:
                self.stderr.write('ignore file [%s]' % (srcPath,))
