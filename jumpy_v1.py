"""
Jumpy v1 is super simple. It looks at the path in front of rex. If there are any pixels that aren't white, rex jumps. Doesn't work so well after some time as the cacti are speeding up.
"""

import os

import cv2
import numpy as np
import pyautogui
from commons.fps import get_start_time, print_fps


# jump position: x = 199, y = 417
# debug position: x = 536 y =  434
# "white" pixels: RGB: (247, 247, 247)
# "black" pixels: RGB: (83, 83, 83)
def get_game_screen():
    os.system("screencapture -x -R133,402,265,35 filename.png")
    im = cv2.imread("filename.png", cv2.IMREAD_GRAYSCALE)
    return im


def main():
    start_time = get_start_time()
    counter = 0
    while True:
        im = get_game_screen()

        pixel_mean = np.mean(im)
        if int(pixel_mean) != 247:
            pyautogui.press("space")
            print("jumpy on", pixel_mean)
        counter = print_fps(start_time, counter)


if __name__ == "__main__":
    main()
