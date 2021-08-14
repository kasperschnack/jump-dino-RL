"""
Jumpy v2 is a first approximation for estimating speed by looking at delta movements of the closest cactus. It creates some issues when cacti come in quick succession where rex doesn't jump. Also speed estimation isn't super precise.
"""

import sys
from timeit import default_timer as timer

import cv2
import numpy as np
import pyautogui
from commons.game_objects import get_cacti_positions, get_game_screen

start = timer()
old_shortest_distance = 0
speeds = []
while 1:
    # read image
    img = get_game_screen()

    rex, super_cacti = get_cacti_positions(img)

    # # show thresh and result
    distances = []
    for super_cactus in super_cacti:
        # x, y, w, h = super_cactus.x, super_cactus.y, super_cactus.w, super_cactus.h
        # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        distance_from_rex = (super_cactus.x + super_cactus.w) - (rex.x + rex.w)
        distances.append(distance_from_rex)
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
    # x, y, w, h = rex.x, rex.y, rex.w, rex.h
    # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    # img = imutils.resize(img, height=200)
    # cv2.imshow("bounding_box", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        sys.exit(0)
cv2.destroyAllWindows()
