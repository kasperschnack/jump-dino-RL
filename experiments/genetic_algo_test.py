import math
import random

import pandas as pd

from commons.genetic_algo import evolve_new_generation


def generate_initial_population():
    for _ in range(7):
        a = random.randint(0, 100)
        b = random.randint(0, 100)
        result = second_order_polynomial_fitness(a, b)
        print(str(a) + "," + str(b) + "," + str(result))


def second_order_polynomial_fitness(a: float, b: float):
    return (
        -((a - 80) ** 2) - (b - 80) ** 2
    )  # taking the sqroot of a negative number complicates things a bit so imma assume we're not gonna choose numbers higher than a=400, b=400 and just let the rest be positive


if __name__ == "__main__":
    prev_pop = pd.read_csv("experiments/sop_initial_population.csv")
    for i in range(300):
        print("GENERATION", i)
        new_pop = evolve_new_generation(prev_pop)
        new_pop["fitness"] = new_pop.apply(
            lambda x: second_order_polynomial_fitness(
                x["initial_jump_distance"], x["score_to_speed_ratio"]
            ),
            axis=1,
        )
        # print(new_pop)
        prev_pop = new_pop.copy()
