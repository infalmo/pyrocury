import json
import os
import statistics
from typing import Callable


def check_correlation(X: list[list[float]], Y: list[list[float]]):
    """
    Given vectors [x1, x2, ...] and [y1, y2, ...], returns the average
    correlation between xi and yi, over all i.
    """
    assert len(X) == len(Y)

    corr = 0
    for i in range(len(X)):
        try:
            corr += statistics.correlation(X[i], Y[i])
        except:
            pass
    return corr / len(X)


def correlation_tester(evaluator: Callable[[str], float]):
    X, Y = [], []
    for f in os.listdir("processed_test_data"):
        data = json.load(open(f"processed_test_data/{f}"))

        x = [st["heat"] for st in data]
        y = [evaluator(st["text"]) for st in data]

        X.append(x)
        Y.append(y)

    print("Correlation:", check_correlation(X, Y))
