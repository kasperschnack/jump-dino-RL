import numpy as np
import pandas as pd
from sklearn.utils import shuffle


def calc_selection_probabilities(df: pd.DataFrame) -> pd.DataFrame:
    # fitness needs to be discounted such that a high fitness score doesn't hoard the probability of being selected
    df["fitness_discounted"] = df["fitness"] ** 0.5
    df["selection_proba"] = df["fitness_discounted"].apply(
        lambda x: x / df["fitness_discounted"].sum()
    )
    return df


def select_from_previous_population(df: pd.DataFrame) -> pd.DataFrame:
    # sample new population
    new_population = df.iloc[np.random.choice(df.index, 6, p=df["selection_proba"])]
    # include the best performer from previous population
    new_population.append(df.iloc[df["fitness"].argmax()])
    # reset fitness
    new_population["fitness"] = 0
    new_population["fitness_discounted"] = 0
    # to counter potential biases when doing other operations we shuffle around the indeces
    new_population = shuffle(new_population).reset_index(drop=True)
    return new_population


def crossover(df: pd.DataFrame) -> pd.DataFrame:
    # decide whether to choose 0, 2 or 4 genes to crossover
    num_of_crossovers = np.random.choice([0, 2, 4], 1, p=[0.6, 0.3, 0.1])[0]
    if num_of_crossovers:
        crossover_genes = df.sample(num_of_crossovers, replace=False)
        # instead of swapping pairwise we'll just shift one down the jump distance
        crossover_genes["initial_jump_distance"] = np.roll(
            crossover_genes["initial_jump_distance"], 1
        )
        df.update(crossover_genes)
    return df


def mutate(val: float) -> float:
    # decide whether to mutate or not
    if np.random.choice([0, 1], 1, p=[0.6, 0.4])[0]:
        val = np.random.gamma(val ** 0.5, val ** 0.5, 1)[0]
    return val or 1


def evolve_new_generation(prev_pop: pd.DataFrame) -> pd.DataFrame:
    prev_pop = calc_selection_probabilities(prev_pop)
    print(prev_pop)
    new_pop = select_from_previous_population(prev_pop)
    new_pop = crossover(new_pop)
    new_pop["initial_jump_distance"] = new_pop["initial_jump_distance"].apply(mutate)
    new_pop["score_to_speed_ratio"] = new_pop["score_to_speed_ratio"].apply(mutate)
    return new_pop
