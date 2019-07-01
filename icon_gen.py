from itertools import product

import numpy as np
import imageio as ii

from PyQt5 import QtWidgets
from PyQt5 import QtGui


W, H = 64, 64

space = np.zeros((H, W, 4), dtype=np.float32)
space[:, :, -1] = 255

HW, HH = int(W / 2), int(H / 2)
OFFSET = int(max(W, H) * 0.42)

px, py = HW, HH
for ox, oy in product(range(-OFFSET, OFFSET + 1), range(-OFFSET, OFFSET + 1)):
    x, y = px + ox, py + oy

    c1 = x > y
    r = 128 if c1 else 255
    g = 255 if c1 else 128
    b = 128 if c1 else 96

    space[x, y] = (r, g, b, 255)


RXF, RXT = HW - OFFSET, HW + OFFSET
RYF, RYT = HH - OFFSET, HH + OFFSET
roll_target = space[RXF: RXT, RYF: RYT, :3]
roll_target = np.roll(roll_target, int(HW * HH * 0.5))
space[RXF: RXT, RYF: RYT, :3] = roll_target

space = space.astype(np.uint8)

ii.imwrite("icon.png", space)

app = QtWidgets.QApplication([])
icon = QtGui.QIcon("icon.png")

print(icon)
