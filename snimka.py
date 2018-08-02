"""
Captures a single image.
"""

import cv2


cap = cv2.VideoCapture(1)

_, frame = cap.read()

cv2.imwrite('result/smimka.jpg', frame)

