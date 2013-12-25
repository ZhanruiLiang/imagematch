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
        Option('-a', '--add', action='store_true', dest='add'),
        Option('--clear', action='store_true', dest='clear'),
        Option('-s', '--status', action='store_true', dest='status'),
        Option('--prefix', action='store', type='string', default='', dest='prefix'),
        Option('--groundtruth', action='store', type='string', dest='groundtruth'),
        Option('--dry', '-n', action='store_true', dest='dry'),
    )

    def handle(self, *args, **options):
        excluding = ('clear', 'add', 'status')
        assert 1 >= sum(bool(options.get(x, None)) for x in excluding)

        if options['clear']:
            assert not options['add']
            self.clear_images_db()

        elif options['add']:
            prefix = options['prefix']
            groundtruthPath = options['groundtruth']
            assert groundtruthPath
            groundtruth = {}
            with open(groundtruthPath) as inf:
                for line in inf:
                    if not line: continue
                    group, name = line.split()
                    group = int(group)
                    groundtruth[name] = group
            for srcPath in args:
                self.import_to_images_db(groundtruth, srcPath, prefix, dry=options['dry'])

        elif options['status']:
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

    def import_to_images_db(self, groundtruth, dir_path, prefix, dry=False):
        if not prefix:
            prefix = datetime.datetime.now().strftime('%m-%d-%H:%M')
        storePath = os.path.join(djsettings.IMAGES_DIR, prefix)
        if not dry:
            if not os.path.exists(storePath):
                os.mkdir(storePath)
        count = 0
        for fname in os.listdir(dir_path):
            srcPath = os.path.join(dir_path, fname)
            ext = os.path.splitext(fname)[1]
            if ext in ('.jpg', '.png'):
                # create new Image instance
                dstPath = os.path.join(storePath, '%s%s'%(count, ext))
                image = Image(path=dstPath, group=groundtruth[fname])
                if not dry:
                    shutil.copy(srcPath, dstPath)
                    image.save()
                self.stdout.write('add [%s] as [%s].' % (srcPath, image.path))
                count += 1
            else:
                self.stderr.write('ignore file [%s]' % (srcPath,))
