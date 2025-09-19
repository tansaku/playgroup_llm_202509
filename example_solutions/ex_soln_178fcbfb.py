import numpy as np


def transform(initial):
    assert isinstance(initial, np.ndarray)

    rows, cols = initial.shape
    final = np.zeros_like(initial)

    # Find all rows with 1 or 3
    rows_1 = np.any(initial == 1, axis=1)
    rows_3 = np.any(initial == 3, axis=1)

    # Process rows with 1 (higher priority)
    for i in range(rows):
        if rows_1[i]:
            final[i, :] = 1

    # Process rows with 3 (lower priority than 1)
    for i in range(rows):
        if rows_3[i] and not rows_1[i]:
            final[i, :] = 3

    # Process columns with 2 (lowest priority)
    cols_2 = np.any(initial == 2, axis=0)
    for j in range(cols):
        if cols_2[j]:
            # Only fill if the cell is not already filled by 1 or 3
            for i in range(rows):
                if final[i, j] == 0:
                    final[i, j] = 2

    assert isinstance(final, np.ndarray)
    return final
