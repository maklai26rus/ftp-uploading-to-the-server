import os
import time
from datetime import datetime, date


def path_normal(path):
    """Модюль преобразующий в правильный путь """
    _pn = os.path.normpath(os.path.join(path))

    return _pn


p = 'dist'
a = os.listdir(p)
files = list(map(path_normal, [os.path.join(p, i) for i in a]))
files = [file for file in files if os.path.isfile(file)]
m = max(files, key=os.path.getmtime)
print(m)
