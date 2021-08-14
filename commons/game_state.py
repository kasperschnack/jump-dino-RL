import os
from os import listdir
from os.path import isfile, join

import cv2
import numpy as np

DIGIT_X_COORS = [1078, 1100, 1122, 1144, 1166]
DIGIT_Y = 18
DIGIT_HEIGHT = 21
DIGIT_WIDTH = 21

GAME_OVER_Y = 83
GAME_OVER_X = 420
GAME_OVER_HEIGHT = 21
GAME_OVER_WIDTH = 381

TEMPLATE_THRESHOLD = 0.99

TEMPLATE_FOLDER_PATH = "./digit_templates/"
DIGIT_TEMPLATES = [
    f for f in listdir(TEMPLATE_FOLDER_PATH) if isfile(join(TEMPLATE_FOLDER_PATH, f))
]


def get_score(img: np.ndarray) -> int:
    assert len(img.shape) == 2  # image has to be grayscale
    number = ""
    for x in DIGIT_X_COORS:
        crop_img = img[DIGIT_Y : DIGIT_Y + DIGIT_HEIGHT, x : x + DIGIT_WIDTH]
        for template_name in DIGIT_TEMPLATES:
            template_path = TEMPLATE_FOLDER_PATH + template_name
            template = cv2.imread(template_path, 0)
            res = cv2.matchTemplate(crop_img, template, cv2.TM_CCOEFF_NORMED)
            if np.amax(res) > TEMPLATE_THRESHOLD:
                number += os.path.splitext(template_name)[0]
    return int(number) if number else 0


def check_if_game_over(img: np.ndarray) -> bool:
    assert len(img.shape) == 2  # image has to be grayscale
    crop_img = img[
        GAME_OVER_Y : GAME_OVER_Y + GAME_OVER_HEIGHT,
        GAME_OVER_X : GAME_OVER_X + GAME_OVER_WIDTH,
    ]
    template = cv2.imread("game_over.png", 0)
    res = cv2.matchTemplate(crop_img, template, cv2.TM_CCOEFF_NORMED)
    if np.amax(res) > TEMPLATE_THRESHOLD:
        return True
    return False


if __name__ == "__main__":
    image = cv2.imread("test2.png", 0)
    print(check_if_game_over(image))
