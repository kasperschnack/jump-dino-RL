"""
Jumpy v4 improves on v3 by sampling starting_jump_distance and the score_to_speed constants and saves data about each run in preparation for later learning based improvements.
"""

import sys
import time

import pyautogui
from commons.fps import get_start_time, print_fps
from commons.game_objects import get_cacti_positions, get_game_coords, get_game_frame
from commons.game_state import check_if_game_over, check_if_rex_in_the_air, get_score

starting_jump_distance = 335
score_to_speed_ratio = 1 / 3
score = 0
start_time = time.time()
freq = 1
counter = 0

x, y = get_game_coords()

while True:
    # read image
    img = get_game_frame(x, y)

    # find object locations
    super_cacti = get_cacti_positions(img)
    distances = [cactus.distance_to_rex for cactus in super_cacti]

    # When reaching checkpoints the score blinks which may result get_score returning 0. To counter wrong behavior use the last known score instead.
    previous_score = score
    score = get_score(img)
    if score == 0:
        score = previous_score

    if check_if_game_over(img) == True:
        print("game over :/")
        print("final score: ", score)
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
