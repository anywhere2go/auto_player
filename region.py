import numpy as np
import mss
import cv2
import time

upleft = (0, 0)
downright = (568, 374)
a,b = upleft
c,d = downright
monitor = {"top": b, "left": a, "width": c, "height": d}

im = np.array(mss.mss().grab(monitor))
screen = cv2.cvtColor(im, cv2.COLOR_BGRA2BGR)

cv2.imshow("Image", im)
print(screen.shape)
#cv2.destroyAllWindows()
