"""
This file unifies the use of the 3 previous ones - crop.py, picture.py and recognize.py.
"""
from PIL import Image
import cv2
import numpy as np
import os


def get_files_in(name):

    """
    Gets the file names of the specified folder(name).
    :param name: A full path of the folder to be traversed.
    :return: list[file names]
    """

    all_files = []

    for directory, subdirectories, files in os.walk(name):
        for filename in files:
            all_files.append('{}{}'.format(name, filename))

    return all_files


templates = get_files_in('src/')


def take_a_pic(name, port):

    """
    Captures a single picture through a specified port.
    :param name: The name of the pick to be saved.
    :param port: The port to be captured through
    :return: void
    """

    if not os.path.exists('result/'):
        os.makedirs('result/')

    cap = cv2.VideoCapture(port)

    _, image = cap.read()

    cv2.imwrite('result/{}.jpg'.format(name), image)


def crop(img_name, coordinates, new_name, show=True):

    """
    Crops an image with a specified name, through specified corners and with specified new name.
    :param img_name: The full name(path) of the image to be cropped.
    :param coordinates: The ((x1,y1),(x2,y2)) coordinates to be used.
    :param new_name: The name in witch the cropped part will be saved.
    :param show: Show the cropped image or not?
    :return: void
    """
    img = Image.open(img_name)
    cropped_image = img.crop(coordinates)
    cropped_image.save('result/cropped_{}.jpg'.format(new_name))

    if show:
        cropped_image.show()


def draw_square(upside, loc, frame, w, h, rect_color=(255, 255, 0), text_color=(0, 255, 0)):
    if upside:
        text = "UPSIDE"
    else:
        text = "DOWNSIDE"
    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), rect_color, 1)
        cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, .7, text_color)


def main(port: int, save_last_frame: bool, crop_last: bool = False):

    """
    The starting point of the program.
    :param port: A port to capture video from.
    :param save_last_frame: Boolean, determines whenever we'll save the last captured frame.
    :param crop_last:
    :return:
    """

    cap = cv2.VideoCapture(port)

    while 1:
        kill = False

        for template_item in templates:
            template = cv2.imread(template_item, 0)
            w, h = template.shape[::-1]
            threshold = 0.9

            _, frame = cap.read()
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            res = cv2.matchTemplate(frame_gray, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res > threshold)

            if template_item.endswith('_up.jpg'):
                draw_square(True, loc, frame, w, h)
            else:
                draw_square(False, loc, frame, w, h)
            cv2.imshow("cam", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                kill = True

                if save_last_frame:
                    cv2.imwrite('result/last_frame.jpg', frame)  # -> save the last captured frame
                break
        if kill:
            break

    cap.release()
    cv2.destroyAllWindows()

    if crop_last and save_last_frame:
        crop('result/last_frame.jpg', (90, 254, 167, 339), 'last')
    if crop_last and not save_last_frame:
        print("Cannot crop a picture that doesn't exist!")


if __name__ == '__main__':
    main(1, True, True)
