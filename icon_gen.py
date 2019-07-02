import os
import math
from itertools import product

import numpy as np
import imageio as ii

from PyQt5 import QtWidgets
from PyQt5 import QtGui


W, H = 64, 64


def clamp(x, y):
    x = min(max(x, 0), W - 1)
    y = min(max(y, 0), H - 1)
    return x, y


space = np.zeros((H, W, 4), dtype=np.float32)
space[:, :, 0] = 1.0
space[:, :, -1] = 1.0

HW, HH = int(W / 2), int(H / 2)

cx, cy = 0, 0

for i in range(100):
    c = math.cos(cx + i) * 32 + 32
    s = math.sin(cy + i) * 32 + 32

    cx, cy = int(c), int(s)

    for ox, oy in product(range(-3, +4), range(-3, +4)):
        cx, cy = clamp(cx + ox, cy + oy)
        space[cx, cy] = (1.0, 1.0, 0.5, 1.0)

space = np.multiply(space, 255.0)
space = space.astype(np.uint8)

if not os.path.isdir("./res"):
    os.makedirs("./res")
ii.imwrite("./res/icon.png", space)

app = QtWidgets.QApplication([])
icon = QtGui.QIcon("./res/icon.png")

print(icon)
