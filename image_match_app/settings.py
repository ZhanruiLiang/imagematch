import os

MAX_SIZE_PER_UPLOAD = 1024 * 1024 * 5 # 5 MB
COMPARER_BIN = os.path.join(os.path.dirname(__file__), 'comparer', 'build', 'comparer')
# Use how many threads to perform the search
WORKER_THREAD_COUNT = 4
# Scale the image before putting it to shared memory ?
SCALE_IMAGE = True
# If SCALE_IMAGE is True, images will be scaled such that max(width, height) = SCALE_TO_LENGTH
SCALE_TO_LENGTH = 120

SHM_SIZE = 100 * 1024 * 1024 # 100 M
