import math

import numpy as np
import pandas as pd
from scipy.stats import mode
from sklearn.metrics import accuracy_score

from linear_regression.linear_regression import normalize


def euclidean_distance(row1, row2) -> float:
    return math.sqrt(sum((row1 - row2) ** 2))


def label_y(y):
    def label(value):
        if value <= 49_999:
            return 0
        elif 50_000 <= value <= 99_999:
            return 1
        elif 100_000 <= value <= 149_999:
            return 2
        elif 150_000 < value <= 199_999:
            return 3
        else:
            return 4

    return np.array([label(item) for item in y])


def find_k(input_data_len: int) -> int:
    k = int(math.sqrt(input_data_len))
    return k if k % 2 == 1 else k + 1


def predict(x_train, y_train , inputs, k):
    output_labels = []
    for i, input in enumerate(inputs):
        point_dist = np.array([euclidean_distance(x, input) for x in x_train])
        dist = np.argsort(point_dist)[:k]
        k_labels = y_train[dist]
        lab = mode(k_labels).mode[0]
        output_labels.append(lab)
        if i % 100 == 0:
            print(i)
    return output_labels


if __name__ == '__main__':
    # Import data
    data_df = pd.read_csv('../data_cleaning/belgrade_selling_flats.csv')
    data_df.dropna(subset=['distance'], inplace=True)
    normalized_data_df = normalize(data_df)

    # Separate training/test sets
    train_df = normalized_data_df.sample(frac=0.7, random_state=0)
    test_df = normalized_data_df.drop(train_df.index)

    x_train = train_df.drop(['price'], axis=1).values
    y_train = train_df['price'].values

    x_test = test_df.drop(['price'], axis=1).values
    y_test = test_df['price'].values

    labeled_y_train = label_y(y_train)
    labeled_y_test = label_y(y_test)
    k = find_k(len(x_train))
    y_predicted = predict(x_train, labeled_y_train, x_test, k)

    print(accuracy_score(labeled_y_test, y_predicted))
