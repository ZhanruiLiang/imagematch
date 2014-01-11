from skimage import color
import numpy as np

X = 256
Y = 32
a = np.zeros((Y, Y, Y, 3), dtype=np.uint8)
for i in xrange(Y):
    a[i, :, :, 0] = i * X / Y
for i in xrange(Y):
    a[:, i, :, 1] = i * X / Y
for i in xrange(Y):
    a[:, :, i, 2] = i * X / Y
# a1 = color.rgb2lab(a)
# result = [(a1[:, :, :, i].min(), a1[:, :, :, i].max()) for i in xrange(3)]

a1 = color.rgb2hsv(a.reshape((Y * Y, Y, 3)))
result = [(a1[:, :, i].min(), a1[:, :, i].max()) for i in xrange(3)]

print result
