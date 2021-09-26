"""
Jumpy v3 improves on v2s speed estimation by using the score as a proxy.
"""

import sys
import time

import pyautogui

from commons.fps import get_start_time, print_fps
from commons.game_objects import get_game_coords, get_game_frame, get_obstacle_positions
from commons.game_state import check_if_game_over, check_if_rex_in_the_air, get_score

starting_jump_distance = 335
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
    distances = [cactus.distance_to_rex for cactus in super_obstacles]

    # When reaching checkpoints the score blinks which may result get_score returning 0. To counter wrong behavior use the last known score instead.
    previous_score = score
    score = get_score(img)
    if score == 0:
        score = previous_score

    if check_if_game_over(img) == True:
        print("game over :/")
        print("final score: ", score)
        sys.exit(0)

    jump_distance = starting_jump_distance + int(score / 3)
    if check_if_rex_in_the_air(img) is False:
        if distances and min(distances) < jump_distance:
            print("Jumping!")
            pyautogui.press("space")
    counter += 1
    if (time.time() - start_time) > freq:
        print("FPS: ", counter / (time.time() - start_time))
        counter = 0
        start_time = time.time()
