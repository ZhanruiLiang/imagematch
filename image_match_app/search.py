import os
from models import Image, QueryImage
from django.conf import settings as djsettings
import settings
import sysv_ipc as ipc
import struct
import threading
import PIL.Image
import subprocess
import time
import random
# import pylab
import comparer

# _cacheLock = threading.Lock()
_imageCache = {}

def get_shm(imageObj):
    """
    image: Image or QueryImage object
    """
    # with _cacheLock:
    if imageObj not in _imageCache:
        if isinstance(imageObj, QueryImage):
            path = imageObj.path.path
        else:
            path = imageObj.path
        image = PIL.Image.open(path)
        w, h = image.size
        if settings.SCALE_IMAGE:
            rateW = settings.SCALE_TO_LENGTH / float(w)
            rateH = settings.SCALE_TO_LENGTH / float(h)
            rate = min(1, rateW, rateH)
            w = int(w * rate)
            h = int(h * rate)
            image = image.resize((w, h))
        size = 8 + w * h * 3
        shm = ipc.SharedMemory(None, flags=ipc.IPC_CREX, size=size)
        shm.write(struct.pack('LL', w, h))
        shm.write(image.tobytes(), offset=8)
        _imageCache[imageObj] = shm
    else:
        shm = _imageCache[imageObj]
    return shm

def clear_cache():
    _imageCache.clear()

def get_likelyhood(targetImg, modelImg):
    shm1 = get_shm(targetImg)
    shm2 = get_shm(modelImg)
    result = comparer.compare(shm1.key, shm1.size, shm2.key, shm2.size)
    return result

def debug_get_likelyhood(queryId, imgId):
    targetImg = QueryImage.objects.get(id=queryId)
    modelImg = Image.objects.get(id=imgId)

    shm1 = get_shm(targetImg)
    shm2 = get_shm(modelImg)

    bin = settings.COMPARER_BIN

    p = subprocess.Popen(
            ['gdb', bin, '--args', bin, str(shm1.key), str(shm1.size), str(shm2.key), str(shm2.size)],
        )
    p.wait()

class Searcher(object):
    """
    After calling search method, these attribute will be available:
        results
        usedTime
        correctRate
    """
    def __init__(self, targetImage):
        self.targetImg = targetImage
        self.startTime = time.time()
        self.results = []
        self.on_finished_single = None
        self.end = False

    def run(self):
        results = self.results
        lock = threading.Semaphore(settings.WORKER_THREAD_COUNT)
        self._error = False

        def add(image):
            with lock:
                if self._error: return
                try:
                    results.append((get_likelyhood(self.targetImg, image), image))
                    if self.on_finished_single:
                        self.on_finished_single()
                except:
                    self._error = True
                    raise

        threads = []
        for image in Image.objects.all():
            with lock:
                if self._error:
                    break
                thread = threading.Thread(target=add, args=(image,))
                thread.start()
                threads.append(thread)
        for thread in threads:
            thread.join()
        results.sort(key=lambda (r, img): -r)
        self.usedTime = time.time() - self.startTime
        if not self._error:
            self.correctRate = self.get_correct_rate()
        else:
            self.correctRate = 0.
        self.end = True

    def get_correct_rate(self):
        # Assume that the first result is identity to the query image
        assert self.results
        group = self.results[0][1].group
        nr = 0 # The count of in group(similar) results
        ans = 0.
        for r, (_, image) in enumerate(self.results):
            if image.group == group:
                nr += 1
                ans += nr / float(r + 1)
        ans /= nr
        return ans

class Tester(object):
    """
    Available attributes:
      correctRates: [(Image, float)]
      groupAverageRates: [(int, float)]
      averageRate: float
    """
    STATE_READY = 'ready'
    STATE_RUNNING = 'running'
    STATE_FINISHED = 'finished'
    STATE_ERROR = 'error'

    def __init__(self, samples_per_group, enabled_groups):
        """
        samples_per_group: Select `samples_per_group` images from imagedb and test
            the correct rate
        enabled_groups: A list of enabled groups to test.
        """
        self.samplesPerGroup = int(samples_per_group)
        self.enabledGroups = enabled_groups
        self.state = self.STATE_READY

    def run(self):
        self.progress = 0.
        self.state = self.STATE_RUNNING
        groups = {g:[] for g in self.enabledGroups}
        images = Image.objects.all()
        for image in images:
            g = image.group
            if g not in groups:
                continue
            groups[g].append(image)
        correctRates = []
        nNeedToCompare = len(images) * len(groups) * self.samplesPerGroup
        nCompared = [0]
        def update_progress():
            # if self.state in (self.STATE_FINISHED, self.STATE_ERROR):
            #     return
            nCompared[0] += 1
            self.progress = '%d / %d' % (nCompared[0], (nNeedToCompare))

        for g, imagesInGroup in groups.iteritems():
            samples = random.sample(imagesInGroup, 
                    min(self.samplesPerGroup, len(imagesInGroup)))
            for image in samples:
                searcher = Searcher(image)
                searcher.on_finished_single = update_progress
                searcher.run()
                r = searcher.correctRate
                correctRates.append((image, r))

        if self.state is not self.STATE_ERROR:
            self.correctRates = correctRates
            self._calculate_average()
            self.state = self.STATE_FINISHED

    def _calculate_average(self):
        groupAverageRates = {}
        total = 0.
        for image, r in self.correctRates:
            g = image.group
            if g not in groupAverageRates:
                groupAverageRates[g] = 0.
            groupAverageRates[g] += r
            total += r
        total /= len(self.correctRates)
        self.groupAverageRates = [(g, r / self.samplesPerGroup) 
                for (g, r) in groupAverageRates.iteritems()]
        self.averageRate = total

