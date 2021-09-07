import os
from typing import Generator

import cv2
import numpy as np
from commons.sprites import Cactus

REX_X_COORD = 52
REX_WIDTH = 80
REX_COLLISION_X_COORD = REX_X_COORD + REX_WIDTH

GAME_CORNER_DIST_FROM_TEMPLATE = 868
GAME_WIDTH = 1200
GAME_HEIGHT = 260
TEMPLATE_THRESHOLD = 0.92

# This function uses "HI" as an anchor point for getting the game screen.
# NOTE: "HI" only appears after playing at least one game.
def get_game_coords() -> tuple:
    os.system("screencapture -x screendump.png")
    screen = cv2.imread("screendump.png", 0)
    template = cv2.imread("./sprites/hi.png", 0)

    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    assert max_val > TEMPLATE_THRESHOLD
    x = max_loc[0] - GAME_CORNER_DIST_FROM_TEMPLATE
    y = max_loc[1]
    return x, y


def get_game_frame(x: int, y: int) -> np.ndarray:
    os.system(
        f"screencapture -x -R{x/2},{y/2},{GAME_WIDTH/2},{GAME_HEIGHT/2} screendump.png"
    )
    return cv2.imread("screendump.png", 0)
    # return cv2.imread("test.png")


def recursive_union_cacti(cacti: list) -> Cactus:
    if len(cacti) > 2:
        return merge_cacti(cacti[0], recursive_union_cacti(cacti[1:]))
    elif len(cacti) == 2:
        return merge_cacti(cacti[0], cacti[1])
    else:
        return cacti[0]


def merge_cacti(a: Cactus, b: Cactus) -> Cactus:
    x = min(a.x, b.x)
    y = min(a.y, b.y)
    w = max(a.x + a.w, b.x + b.w) - x
    h = max(a.y + a.h, b.y + b.h) - y
    distance_to_rex = max(a.distance_to_rex, b.distance_to_rex)
    return Cactus(x, y, w, h, distance_to_rex)


def group_close_cacti(cacti: list) -> Generator:
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


def get_cacti_positions(img: np.ndarray) -> list:
    # invert image
    img = 255 - img

    # threshold
    thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)[1]

    # get contours
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    cacti = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # filtering contours
            x, y, w, h = cv2.boundingRect(cnt)
            if (
                y > 112
            ):  # the highest flying pterodactyls can't be jumped over so we just want to ignore those
                if w / h < 4:  # filtering even more
                    distance_to_rex = x + w - REX_COLLISION_X_COORD
                    if distance_to_rex > w:
                        cacti.append(Cactus(x, y, w, h, distance_to_rex))

    cacti_clusters = list(group_close_cacti(cacti))
    super_cacti = []

    for cacti_cluster in cacti_clusters:
        super_cactus = recursive_union_cacti(cacti_cluster)
        super_cacti.append(super_cactus)

    return super_cacti


if __name__ == "__main__":
    x, y = get_game_coords()
    get_game_frame(x, y)
