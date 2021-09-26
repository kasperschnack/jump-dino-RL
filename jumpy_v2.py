"""
Jumpy v2 is a first approximation for estimating speed by looking at delta movements of the closest obstacle. It creates some issues when obstacles come in quick succession where rex doesn't jump. Also speed estimation isn't super precise.
"""

import sys
from timeit import default_timer as timer

import cv2
import numpy as np
import pyautogui

from commons.game_objects import get_game_coords, get_game_frame, get_obstacle_positions

start = timer()
old_shortest_distance = 0
speeds = []
x, y = get_game_coords()
while 1:
    # read image
    img = get_game_frame(x, y)
    super_obstacles = get_obstacle_positions(img)

    distances = [obstacle.distance_to_rex for obstacle in super_obstacles]
    if distances:
        shortest_distance = min(distances)
    if shortest_distance != 0 and shortest_distance < old_shortest_distance:
        current_speed = old_shortest_distance - shortest_distance
        speeds.append(current_speed)
    old_shortest_distance = shortest_distance
    jump_distance = 335 + np.average(speeds[-10:]) / 2
    print(jump_distance)
    if shortest_distance < jump_distance:
        pyautogui.press("space")
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        sys.exit(0)
cv2.destroyAllWindows()
