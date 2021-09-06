"""
Jumpy v1 is super simple. It looks at the path in front of rex. If there are any pixels that aren't white, rex jumps. Doesn't work so well after some time as the cacti are speeding up.
"""
import numpy as np
import pyautogui
from commons.fps import get_start_time, print_fps
from commons.game_objects import get_game_coords, get_game_frame

look_zone = 285, 190, 114, 39

# "white" pixels: RGB: (247, 247, 247)
# "black" pixels: RGB: (83, 83, 83)
def main():
    x, y = get_game_coords()
    start_time = get_start_time()
    counter = 0
    while True:
        im = get_game_frame(x, y)
        crop_img = im[
            look_zone[1] : look_zone[1] + look_zone[3],
            look_zone[0] : look_zone[0] + look_zone[2],
        ]
        pixel_mean = np.mean(crop_img)
        if int(pixel_mean) != 247:
            pyautogui.press("space")
            print("jumpy on", pixel_mean)
        counter = print_fps(start_time, counter)


if __name__ == "__main__":
    main()
