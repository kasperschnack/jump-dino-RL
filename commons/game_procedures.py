import sys
import time

import cv2
import imutils
import pandas as pd
import pyautogui

from commons.game_objects import (
    check_if_rex_in_the_air,
    get_game_coords,
    get_game_frame,
    get_obstacle_positions,
    get_rex_position,
)
from commons.game_state import check_if_game_over, get_score


def play_out_population(df: pd.DataFrame, population_name: str) -> pd.DataFrame:
    for _, row in df.iterrows():
        row["fitness"] = play_single_game(
            row["initial_jump_distance"], row["score_to_speed_ratio"]
        )
    df.to_csv(population_name)


def play_single_game(
    initial_jump_distance: int, score_to_speed_ratio: float, debug_mode: bool = False
) -> int:
    x, y = get_game_coords()
    score = 0
    start_time = time.time()
    freq = 1
    counter = 0
    if debug_mode:
        cv2.namedWindow("debug_window")
        cv2.moveWindow("debug_window", 720, 0)

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
        super_obstacles = get_obstacle_positions(img)
        distances = [obstacle.distance_to_rex for obstacle in super_obstacles]

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
        if distances and min(distances) < jump_distance:
            if not check_if_rex_in_the_air(img):
                print("Jumping!")
                pyautogui.press("space")
        counter += 1
        if (time.time() - start_time) > freq:
            print("FPS: ", counter / (time.time() - start_time))
            counter = 0
            start_time = time.time()
        if debug_mode:
            display_game(img, super_obstacles, distances)
    return score


def display_game(img, obstacles, distances):
    rex = get_rex_position(img)
    cv2.rectangle(img, (rex.x, rex.y), (rex.x + rex.w, rex.y + rex.h), (0, 255, 0), 1)
    for obstacle in obstacles:
        x, y, w, h = obstacle.x, obstacle.y, obstacle.w, obstacle.h
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
    img = imutils.resize(img, width=720)
    if distances:
        cv2.putText(
            img,
            str(min(distances)),
            (0, 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1,
            cv2.LINE_AA,
        )
    cv2.imshow("debug_window", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        sys.exit(0)


if __name__ == "__main__":
    play_single_game(320, 0.175, True)
