import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def normalize(df):
    result = df.copy()
    for feature_name in ['room_number', 'square_footage', 'floor', 'distance', 'elevator', 'balcony', 'registered']:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result


def cost_function(x, y, w, b):
    return np.sum((((x.dot(w) + b) - y) ** 2) / (2 * len(y)))


def gradient_descent(x, y, w, b, learning_rate, epochs):
    cost_list = [0] * epochs

    for epoch in range(epochs):
        z = x.dot(w) + b
        loss = z - y

        weight_gradient = x.T.dot(loss) / len(y)
        bias_gradient = np.sum(loss) / len(y)

        w = w - learning_rate * weight_gradient
        b = b - learning_rate * bias_gradient

        cost = cost_function(x, y, w, b)
        cost_list[epoch] = cost

        if epoch % (epochs / 100) == 0:
            # plt.plot(cost_list)
            # plt.pause(0.000001)
            print(f"Cost is: {cost}")

    return w, b, cost_list


def r2score(y_pred, y):
    rss = np.sum((y_pred - y) ** 2)
    tss = np.sum((y - y.mean()) ** 2)

    r2 = 1 - (rss / tss)
    return r2


def predict(X, w, b):
    return X.dot(w) + b


def linear_regression_prediction(X):
    with open('../price_prediction_app/parameters.json', 'r') as file:
        params = json.load(file)

    w = np.array([
        float(params['w_room_number']),
        float(params['w_square_footage']),
        float(params['w_floor']),
        float(params['w_elevator']),
        float(params['w_balcony']),
        float(params['w_registered']),
        float(params['w_distance'])
    ])

    return X.dot(w) + float(params['bias'])


def dump_parameters(file, weights, bias):
    params = {
        'bias': bias,
        'w_room_number': weights[0],
        'w_square_footage': weights[1],
        'w_floor': weights[2],
        'w_elevator': weights[3],
        'w_balcony': weights[4],
        'w_registered': weights[5],
        'w_distance': weights[6]
    }
    with open(file, 'w') as out_file:
        json.dump(params, out_file)


if __name__ == '__main__':
    # Import data
    data_df = pd.read_csv('../data_cleaning/belgrade_selling_flats.csv')
    data_df.dropna(subset=['distance'], inplace=True)
    normalized_data_df = normalize(data_df)

    # Separate training/test sets
    train_df = normalized_data_df.sample(frac=0.75, random_state=0)
    test_df = normalized_data_df.drop(train_df.index)

    x_train = train_df.drop(['price'], axis=1).values
    y_train = train_df['price'].values

    x_test = test_df.drop(['price'], axis=1).values
    y_test = test_df['price'].values

    # Train
    w, b, c = gradient_descent(x_train, y_train, np.zeros(x_train.shape[1]), 0, 0.0053, epochs=140000)
    dump_parameters('parameters.json', w, b)

    y_pred = predict(x_test, w, b)

    print(f"r2 score: {r2score(y_pred, y_test)}")
