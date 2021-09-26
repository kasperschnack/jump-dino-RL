"""
Jumpy v4 improves on v3 by sampling starting_jump_distance and the score_to_speed constants and saves data about each run in preparation for later learning based improvements.
"""

import sys
import time

import numpy as np
import pyautogui

from commons.fps import get_start_time, print_fps
from commons.game_objects import (
    check_if_rex_in_the_air,
    get_game_coords,
    get_game_frame,
    get_obstacle_positions,
)
from commons.game_state import check_if_game_over, get_score
from commons.io_utils import store_data

starting_jump_distance = int(np.random.normal(300, 30))
score_to_speed_ratio = np.random.normal(1 / 3, 1 / 3)
print(f"starting_jump_distance: {starting_jump_distance}")
print(f"score_to_speed_ratio: {score_to_speed_ratio}")
score = 0
start_time = time.time()
freq = 1
counter = 0

x, y = get_game_coords()

while True:
    # read image
    img = get_game_frame(x, y)

    # find object locations
    super_obstacles = get_obstacle_positions(img)
    distances = [obstacle.distance_to_rex for obstacle in super_obstacles]

    # When reaching checkpoints the score blinks which may result get_score returning 0. To counter wrong behavior use the last known score instead.
    previous_score = score
    score = get_score(img)
    if score == 0:
        score = previous_score

    if check_if_game_over(img) == True:
        print("game over :/")
        print(f"final score: {score}")
        data = [score, starting_jump_distance, score_to_speed_ratio]
        store_data(data, "jumpy_v4")
        sys.exit(0)

    jump_distance = starting_jump_distance + int(score_to_speed_ratio * score)
    if check_if_rex_in_the_air(img) is False:
        if distances and min(distances) < jump_distance:
            print("Jumping!")
            pyautogui.press("space")
    counter += 1
    if (time.time() - start_time) > freq:
        print("FPS: ", counter / (time.time() - start_time))
        counter = 0
        start_time = time.time()
