import os

MAX_SIZE_PER_UPLOAD = 1024 * 1024 * 5 # 5 MB
COMPARER_BIN = os.path.join(os.path.dirname(__file__), 'comparer', 'build', 'comparer')
