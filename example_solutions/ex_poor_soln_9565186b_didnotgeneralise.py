import numpy as np


def transform(initial):
    assert isinstance(initial, np.ndarray)

    final = initial.copy()
    rows, cols = initial.shape

    # Identify pure rows (all elements equal)
    pure_rows = []
    for i in range(rows):
        if np.all(initial[i] == initial[i][0]):
            pure_rows.append(initial[i][0])

    for i in range(rows):
        # Skip pure rows (they remain unchanged)
        if np.all(initial[i] == initial[i][0]):
            continue

        # Check if row contains an 8
        if 8 in initial[i]:
            for j in range(cols):
                # Keep values that match any pure row's value, else set to 5
                if initial[i][j] not in pure_rows:
                    final[i][j] = 5
        else:
            # For rows without 8s, set all non-pure-matching values to 5
            for j in range(cols):
                if initial[i][j] not in pure_rows:
                    final[i][j] = 5

    assert isinstance(final, np.ndarray)
    return final
