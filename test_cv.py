import numpy as np
import cv2 as cv
im = cv.imread('chat_box.png')
cv.imshow("chat_box",im)
cv.waitKey(0)
cv.destroyAllWindows()

#pip install opencv-python==4.5.1.48