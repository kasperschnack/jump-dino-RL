"""
Jumpy v1 is super simple. It looks at the path in front of rex. If there are any pixels that aren't white, rex jumps. Doesn't work so well after some time as the cacti are speeding up.

"""

import pyautogui
import os
import cv2
import numpy as np
from timeit import default_timer as timer

# jump position: x = 199, y = 417
# debug position: x = 536 y =  434
# "white" pixels: RGB: (247, 247, 247)
# "black" pixels: RGB: (83, 83, 83)
def get_game_screen():
    os.system("screencapture -x -R55,305,130,610 filename.png")
    im = cv2.imread("filename.png", cv2.IMREAD_GRAYSCALE)
    return im


def print_fps(start_time, counter, x):
    if (timer() - start_time) > x:
        print("FPS: ", counter / (timer() - start_time))
        # print(pixel_value)
        counter = 0
        start_time = timer()
    return counter


def main():
    start_time = timer()
    x = 1  # displays the frame rate every 1 second
    counter = 0
    while True:
        im = get_game_screen()

        pixel_mean = np.mean(im)
        if int(pixel_mean) != 247:
            pyautogui.press("space")
            print("jumpy on", pixel_mean)
        counter += 1
        print_fps(start_time, counter, x)


if __name__ == "__main__":
    main()
