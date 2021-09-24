"""
Jumpy v5 introduces actual learning with the Genetic Algorithmic approaches of selection, crossover and mutation.
"""

import pandas as pd

from commons.game_procedures import play_out_population

test_population = pd.read_csv("test_population.csv")

play_out_population(test_population, "test_pop_1")
