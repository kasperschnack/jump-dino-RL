"""
Jumpy v5 introduces actual learning with the Genetic Algorithmic approaches of selection, crossover and mutation.
"""

import numpy as np

from commons.game_procedures import play_single_game

initial_jump_distance = int(np.random.normal(300, 30))
score_to_speed_ratio = np.random.normal(1 / 3, 1 / 3)
print(f"starting_jump_distance: {initial_jump_distance}")
print(f"score_to_speed_ratio: {score_to_speed_ratio}")

play_single_game(initial_jump_distance, score_to_speed_ratio)
