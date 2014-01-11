import numpy as np
import PIL.Image
import settings
from models import QueryImage
from skimage import color

class RGBComparer:
    BINS = [1 << 6, 1 << 6, 1 << 6]
    RANGES = [(0, 256), (0, 256), (0, 256)]
    # WEIGHTS = (0.2126, 0.7152, 0.0722)
    WEIGHTS = (1., 1., 1.)

    @classmethod
    def compare(cls, img1, img2):
        data1 = cls.get_image_data(img1)
        data2 = cls.get_image_data(img2)
        result = 0
        for level in range(3):
            result += cls.WEIGHTS[level] * np.sum(np.minimum(data1[level], data2[level]))
        return result

    @classmethod
    def make_histograms(cls, data):
        data = cls.convert(data)
        n = float(np.prod(data.shape[:2]))
        return tuple(
            np.histogram(data[:, :, level], bins=bins, range=ranges)[0] / n
            for (level, bins, ranges) in zip(range(3), cls.BINS, cls.RANGES)
        )

    @classmethod
    def convert(cls, data):
        return data

    _imageCache = {}

    @classmethod
    def get_image_data(cls, imageObj):
        """
        image: Image or QueryImage object
        """
        _imageCache = cls._imageCache
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
            data = cls.make_histograms(np.array(image))
            _imageCache[imageObj] = data
        else:
            data = _imageCache[imageObj]
        return data


class LabComparer(RGBComparer):
    BINS = [30, 30, 30]
    RANGES = [
        (0.0, 100.0),
        (-86.183029744395014, 98.233053863113156),
        (-107.85730020669489, 94.478122276478231)
    ]
    WEIGHTS = [1., 1., 1.]

    @classmethod
    def convert(cls, data):
        return color.rgb2lab(data)


class HSVComparer(RGBComparer):
    # BINS = [50, 30, 30]
    BINS = [100, 80, 80]
    RANGES = [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0)]
    WEIGHTS = [1., 1., 1.]

    @classmethod
    def convert(cls, data):
        return color.rgb2hsv(data)


class TunedHSVComparer(HSVComparer):
    BINS = [100, 80, 80, 100]
    RANGES = [(0.0, 1.0), (0.0, 1.0), (0.0, 1.0)]
    WEIGHTS = [1., 1., 1., 1.]

    @classmethod
    def make_histograms(cls, data):
        data = cls.convert(data)
        hists = []
        n = float(np.prod(data.shape[:2]))

        for (level, bins, ranges) in zip(range(3), cls.BINS, cls.RANGES):
            hists.append(
                np.histogram(data[:, :, level], bins=bins, range=ranges)[0] / n
            )
        hists.append(
            np.histogram(
                (.5 + data[:, :, 0]) % 1,
                bins=cls.BINS[0],
                range=cls.RANGES[0],
            )[0] / n
        )
        # print(hists)
        # assert 0
        return tuple(hists)

    @classmethod
    def compare(cls, img1, img2):
        data1 = cls.get_image_data(img1)
        data2 = cls.get_image_data(img2)
        result = 0.
        for level in range(4):
            result += cls.WEIGHTS[level] * np.sum(np.minimum(data1[level], data2[level]))
        return result

# comparer = RGBComparer
# comparer = LabComparer
comparer = HSVComparer
# comparer = TunedHSVComparer
