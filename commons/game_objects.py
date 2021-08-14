import os

import cv2
import numpy as np
from sprites import Cactus, Rex


def get_game_screen():
    os.system("screencapture -x -R55,305,610,160 filename.png")
    return cv2.imread("filename.png")
    # return cv2.imread("test.png")


def recursive_union_cacti(cacti: list) -> list:
    if len(cacti) > 2:
        return merge_cacti(cacti[0], recursive_union_cacti(cacti[1:]))
    elif len(cacti) == 2:
        return merge_cacti(cacti[0], cacti[1])
    elif len(cacti) == 1:
        return cacti[0]
    else:
        return []


def merge_cacti(a: Cactus, b: Cactus) -> Cactus:
    x = min(a.x, b.x)
    y = min(a.y, b.y)
    w = max(a.x + a.w, b.x + b.w) - x
    h = max(a.y + a.h, b.y + b.h) - y
    return Cactus(x, y, w, h)


def group_close_cacti(cacti: list) -> list:
    cacti.sort(key=lambda x: x.horizontal_center)
    prev = None
    group = []
    for cactus in cacti:
        if not prev or cactus.horizontal_center - prev.horizontal_center <= 60:
            group.append(cactus)
        else:
            yield group
            group = [cactus]
        prev = cactus
    if group:
        yield group


rex_x_coord = 62
rex_width = 80
rex_collision_x_coord = rex_x_coord + rex_width
cv2.namedWindow("bounding_box")
cv2.moveWindow("bounding_box", 720, 0)


def get_game_objects(img: np.ndarray) -> tuple:
    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # invert image
    gray = 255 - gray

    # threshold
    thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)[1]

    # get contours
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    rex = {}
    cacti = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # filtering contours
            x, y, w, h = cv2.boundingRect(cnt)
            if w / h < 4:  # filtering even more
                distance_to_rex = x - rex_collision_x_coord
                if distance_to_rex > 0:
                    cacti.append(Cactus(x, y, w, h))
                else:
                    rex = Rex(x, y, w, h)

    cacti_clusters = list(group_close_cacti(cacti))
    super_cacti = []

    for cacti_cluster in cacti_clusters:
        super_cactus = recursive_union_cacti(cacti_cluster)
        super_cacti.append(super_cactus)

    return rex, super_cacti
