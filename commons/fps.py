from timeit import default_timer as timer


def get_start_time() -> float:
    return timer()


def print_fps(start_time: float, counter: int, freq: int = 1) -> float:
    if (timer() - start_time) > freq:
        print("FPS: ", counter / (timer() - start_time))
        counter = 0
        return timer()
    return start_time
