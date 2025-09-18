import numpy as np


def transform(initial):
    assert isinstance(initial, np.ndarray)
    # Define the mapping
    digit_mapping = {0: 0, 1: 5, 2: 6, 3: 4, 4: 3, 5: 1, 6: 2, 7: 7, 8: 9, 9: 8}

    # Apply the mapping to each element in the grid
    final = np.vectorize(digit_mapping.get)(initial)

    assert isinstance(final, np.ndarray)
    return final
