import numpy as np
import pandas as pd
from sklearn.utils import shuffle


def calc_selection_probabilities(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("fitness", ascending=False, ignore_index=True)
    df["rank"] = df.index + 1
    df["scaled_fitness"] = 1 / df["rank"] ** 0.5 / len(df)
    df["selection_proba"] = df["scaled_fitness"] / df["scaled_fitness"].sum()
    return df


def select_from_previous_population(df: pd.DataFrame) -> pd.DataFrame:
    # sample new population
    new_population = df.iloc[np.random.choice(df.index, 6, p=df["selection_proba"])]
    # include the best performer from previous population
    new_population.append(df.iloc[df["fitness"].argmax()])
    # reset fitness
    new_population = new_population.drop(
        columns=["fitness", "rank", "scaled_fitness", "selection_proba"]
    )
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
        val = np.random.normal(val, 1, 1)[0]
    return val or 1


def evolve_new_generation(prev_pop: pd.DataFrame) -> pd.DataFrame:
    prev_pop = calc_selection_probabilities(prev_pop)
    print(prev_pop)
    new_pop = select_from_previous_population(prev_pop)
    new_pop = crossover(new_pop)
    new_pop["initial_jump_distance"] = new_pop["initial_jump_distance"].apply(mutate)
    new_pop["score_to_speed_ratio"] = new_pop["score_to_speed_ratio"].apply(mutate)
    return new_pop
