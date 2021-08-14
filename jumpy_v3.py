"""
Jumpy v3 improves on v2s speed estimation by using the score as a proxy.
"""

import pdb
import sys
import traceback

import cv2
import pyautogui
from commons.game_objects import get_game_objects, get_game_screen
from commons.score import get_score

starting_jump_distance = 345
score = 0

while 1:
    # read image
    img = get_game_screen()

    # find object locations
    rex, super_cacti = get_game_objects(img)

    # get current score
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # When reaching checkpoints the score blinks which may result get_score returning 0. To counter wrong behavior use the last known score instead.
    previous_score = score
    score = get_score(img_gray)
    if score == 0:
        score = previous_score

    # # show thresh and result
    distances = []
    for super_cactus in super_cacti:
        # x, y, w, h = super_cactus.x, super_cactus.y, super_cactus.w, super_cactus.h
        # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        try:
            distance_from_rex = (super_cactus.x + super_cactus.w) - (rex.x + rex.w)
            distances.append(distance_from_rex)
        except:
            extype, value, tb = sys.exc_info()
            traceback.print_exc()
            pdb.post_mortem(tb)
    jump_distance = starting_jump_distance + int(score / 3)
    if any(dist < jump_distance for dist in distances):
        print("jump!")
        pyautogui.press("space")
    print("Distances", distances)
    print("Jump distance", jump_distance)
    # x, y, w, h = rex.x, rex.y, rex.w, rex.h
    # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    # img = imutils.resize(img, height=200)
    # cv2.imshow("bounding_box", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        sys.exit(0)
cv2.destroyAllWindows()
