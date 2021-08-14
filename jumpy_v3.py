"""
Jumpy v3 improves on v2s speed estimation by using the score as a proxy.
"""

import sys

import cv2
import pyautogui
from commons.game_objects import get_cacti_positions, get_game_screen
from commons.game_state import check_if_game_over, get_score

starting_jump_distance = 345
score = 0

while 1:
    # read image
    img = get_game_screen()

    # find object locations
    super_cacti = get_cacti_positions(img)

    # get current score
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # When reaching checkpoints the score blinks which may result get_score returning 0. To counter wrong behavior use the last known score instead.
    previous_score = score
    score = get_score(img_gray)
    if score == 0:
        score = previous_score

    if check_if_game_over(img_gray) == True:
        sys.exit(0)

    jump_distance = starting_jump_distance + int(score / 3)
    distances = [cactus.distance_to_rex for cactus in super_cacti]
    print("Distances", distances)
    print("Jump distance", jump_distance)
    if any(dist < jump_distance for dist in distances):
        print("jump!")
        pyautogui.press("space")
    # x, y, w, h = rex.x, rex.y, rex.w, rex.h
    # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    # img = imutils.resize(img, height=200)
    # cv2.imshow("bounding_box", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        sys.exit(0)
cv2.destroyAllWindows()
