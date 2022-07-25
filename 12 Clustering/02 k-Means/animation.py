import pandas as pd
import numpy as np


def create_animation(data, fun, k):
    result = {
        'x': [],
        'y': [],
        'type': [],
        'class': [],
        'group': [],
        'frame': []
    }

    for i, (centroids_x, centroids_y) in enumerate(fun(data['x'], data['y'], k=k), 1):
        result['x'].extend(data['x'].tolist())
        result['y'].extend(data['y'].tolist())
        result['type'].extend((0.1 for _ in range(len(data['x']))))

        for x, y in zip(data['x'], data['y']):
            distances = np.sqrt((centroids_x - x) ** 2 + (centroids_y - y) ** 2)
            result['class'].append(str(distances.argmin() + 1))

        result['x'].extend(centroids_x)
        result['y'].extend(centroids_y)
        result['type'].extend((0.5 for _ in range(len(centroids_x))))
        result['class'].extend(map(str, range(1, len(centroids_x) + 1)))

        combined_length = len(data['x']) + len(centroids_x)
        result['group'].extend(range(combined_length))
        result['frame'].extend((i for _ in range(combined_length)))

        if i >= 30:
            break

    return pd.DataFrame(result)
