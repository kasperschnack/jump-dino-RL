import os
from typing import Generator

import cv2
import numpy as np

from commons.sprites import Obstacle, Rex

REX_X_COORD = 52
REX_Y_COORD = 190
REX_WIDTH = 80
REX_HEIGHT = 70

REX_COLLISION_X_COORD = REX_X_COORD + REX_WIDTH

GAME_CORNER_DIST_FROM_TEMPLATE_X = 868
GAME_CORNER_DIST_FROM_TEMPLATE_Y = 20
GAME_WIDTH = 1200
GAME_HEIGHT = 276
TEMPLATE_THRESHOLD = 0.92

REX_TEMPLATE = cv2.imread("./sprites/rex.png", 0)

# This function uses "HI" as an anchor point for getting the game screen.
# NOTE: "HI" only appears after playing at least one game.
def get_game_coords() -> tuple:
    os.system("screencapture -x screendump.png")
    screen = cv2.imread("screendump.png", 0)
    template = cv2.imread("./sprites/hi.png", 0)

    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    assert max_val > TEMPLATE_THRESHOLD
    x = max_loc[0] - GAME_CORNER_DIST_FROM_TEMPLATE_X
    y = max_loc[1] - GAME_CORNER_DIST_FROM_TEMPLATE_Y
    return x, y


def get_game_frame(x: int, y: int) -> np.ndarray:
    os.system(
        f"screencapture -x -R{x/2},{y/2},{GAME_WIDTH/2},{GAME_HEIGHT/2} screendump.png"
    )
    return cv2.imread("screendump.png", 0)
    # return cv2.imread("test.png")


def recursive_union_obstacles(obstacles: list) -> Obstacle:
    if len(obstacles) > 2:
        return merge_obstacles(obstacles[0], recursive_union_obstacles(obstacles[1:]))
    elif len(obstacles) == 2:
        return merge_obstacles(obstacles[0], obstacles[1])
    else:
        return obstacles[0]


def merge_obstacles(a: Obstacle, b: Obstacle) -> Obstacle:
    x = min(a.x, b.x)
    y = min(a.y, b.y)
    w = max(a.x + a.w, b.x + b.w) - x
    h = max(a.y + a.h, b.y + b.h) - y
    distance_to_rex = max(a.distance_to_rex, b.distance_to_rex)
    return Obstacle(x, y, w, h, distance_to_rex)


def group_close_obstacles(obstacles: list) -> Generator:
    obstacles.sort(key=lambda x: x.horizontal_center)
    prev = None
    group = []
    for obstacle in obstacles:
        if not prev or obstacle.horizontal_center - prev.horizontal_center <= 60:
            group.append(obstacle)
        else:
            yield group
            group = [obstacle]
        prev = obstacle
    if group:
        yield group


def get_rex_position(img: np.ndarray) -> Rex:
    assert (
        len(img.shape) == 2
    )  # image has to be grayscale for template matching to work
    crop_img = img[
        0:GAME_HEIGHT,
        REX_X_COORD : REX_X_COORD + REX_WIDTH,
    ]

    res = cv2.matchTemplate(crop_img, REX_TEMPLATE, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    assert max_val > TEMPLATE_THRESHOLD
    y = max_loc[1]
    return Rex(REX_X_COORD, y, REX_WIDTH, REX_HEIGHT)


def check_if_rex_in_the_air(img: np.ndarray) -> bool:
    assert len(img.shape) == 2  # image has to
    crop_img = img[
        REX_Y_COORD : REX_Y_COORD + REX_HEIGHT,
        REX_X_COORD : REX_X_COORD + REX_WIDTH,
    ]
    template = cv2.imread("./sprites/rex.png", 0)
    res = cv2.matchTemplate(crop_img, template, cv2.TM_CCOEFF_NORMED)
    if np.amax(res) > TEMPLATE_THRESHOLD:
        return False
    return True


def get_obstacle_positions(img: np.ndarray) -> list:
    # invert image
    img = 255 - img

    # threshold
    thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)[1]

    # get contours
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    obstacles = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # filtering contours
            x, y, w, h = cv2.boundingRect(cnt)
            if (
                y > 118
            ):  # the highest flying pterodactyls can't be jumped over so we just want to ignore those
                if w / h < 4:  # filtering even more
                    distance_to_rex = x + w - REX_COLLISION_X_COORD
                    if distance_to_rex > w:
                        obstacles.append(Obstacle(x, y, w, h, distance_to_rex))

    obstacles_clusters = list(group_close_obstacles(obstacles))
    super_obstacles = []

    for obstacles_cluster in obstacles_clusters:
        super_obstacle = recursive_union_obstacles(obstacles_cluster)
        super_obstacles.append(super_obstacle)

    return super_obstacles


if __name__ == "__main__":
    x, y = get_game_coords()
    get_game_frame(x, y)
