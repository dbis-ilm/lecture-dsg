import pandas as pd


def create_animation(data, fun, eps, min_pts):
    result = {
        'x': [],
        'y': [],
        'class': [],
        'group': [],
        'frame': []
    }

    xs = data['x']
    ys = data['y']

    for i, clusters in enumerate(fun(data['x'], data['y'], eps=eps, min_pts=min_pts), 1):
        result['x'].extend(xs.tolist())
        result['y'].extend(ys.tolist())
        result['class'].extend(map(str, clusters))
        result['group'].extend(range(1, len(xs) + 1))
        result['frame'].extend((i for _ in range(len(data['x']))))

    classes = set(clusters)
    i = 0

    while i < len(result['x']):
        for cl in classes:
            result['x'].insert(i, 0)
            result['y'].insert(i, 0)
            result['class'].insert(i, str(cl))
            result['group'].insert(i, -cl)
            result['frame'].insert(i, result['frame'][i])

        i += len(xs) + len(classes)

    return pd.DataFrame(result), (xs.min() - 1, xs.max() + 1), (ys.min() - 1, ys.max() + 1)
