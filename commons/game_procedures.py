import time

import pandas as pd
import pyautogui

from commons.game_objects import get_cacti_positions, get_game_coords, get_game_frame
from commons.game_state import check_if_game_over, check_if_rex_in_the_air, get_score
from commons.io_utils import store_data


def play_out_population(df: pd.DataFrame, population_name: str) -> pd.DataFrame:
    for _, row in df.iterrows():
        row["fitness"] = play_single_game(
            row["initial_jump_distance"], row["score_to_speed_ratio"]
        )
    df.to_csv(population_name)


def play_single_game(initial_jump_distance: int, score_to_speed_ratio: float) -> int:
    x, y = get_game_coords()
    score = 0
    start_time = time.time()
    freq = 1
    counter = 0

    # reset game if starting a new one
    img = get_game_frame(x, y)
    if check_if_game_over(img):
        print("Resetting game!")
        pyautogui.moveTo(360, 400)
        pyautogui.click()
        pyautogui.click()

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

        if check_if_game_over(img):
            print("game over :/")
            print(f"final score: {score}")
            break

        jump_distance = initial_jump_distance + int(score_to_speed_ratio * score)
        if check_if_rex_in_the_air(img) is False:
            if distances and min(distances) < jump_distance:
                print("Jumping!")
                pyautogui.press("space")
        counter += 1
        if (time.time() - start_time) > freq:
            print("FPS: ", counter / (time.time() - start_time))
            counter = 0
            start_time = time.time()
    return score
