from collections import deque

import numpy as np


def transform(initial):
    assert isinstance(initial, np.ndarray)

    rows, cols = initial.shape
    visited = np.zeros_like(initial, dtype=bool)
    final = np.zeros_like(initial)
    region_num = 0

    for i in range(rows):
        for j in range(cols):
            if initial[i, j] == 5 and not visited[i, j]:
                region_num += 1
                queue = deque([(i, j)])
                visited[i, j] = True

                while queue:
                    x, y = queue.popleft()
                    final[x, y] = region_num

                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < rows and 0 <= ny < cols:
                            if initial[nx, ny] == 5 and not visited[nx, ny]:
                                visited[nx, ny] = True
                                queue.append((nx, ny))

    assert isinstance(final, np.ndarray)
    return final
