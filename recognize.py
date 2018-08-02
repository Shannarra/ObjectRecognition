"""
Draws squares around a bottle cap in real-time video.
"""

import cv2
import numpy as np


def draw(upside):
    if upside:
        text = "UPSIDE"
    else:
        text = "DOWNSIDE"
    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (255, 255, 0), 1)
        cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, .7, (0, 255, 0))


cap = cv2.VideoCapture(1)

templates = [
    'src/hello2_up.jpg',
    'src/hello2_down.jpg',
    'src/hello3_up.jpg',
    'src/hello3_down.jpg'
]

while 1:
    kill = False

    for templ in templates:
        template = cv2.imread(templ, 0)
        w, h = template.shape[::-1]
        threshold = 0.9

        _, frame = cap.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(frame_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res > threshold)

        if templ.endswith('_up.jpg'):
            draw(True)
        else:
            draw(False)
        cv2.imshow("cam", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            kill = True
            cv2.imwrite('result/hello2.jpg', frame)  # -> save the last captured frame
            break
    if kill:
        break


cap.release()
cv2.destroyAllWindows()
