import json
import urllib.parse
import urllib.request
from tkinter import Tk, Label, Button, Entry, StringVar, Radiobutton, IntVar, Checkbutton

import numpy as np

from knn.knn import knn_prediction
from linear_regression.linear_regression import linear_regression_prediction

master = Tk()
algorithm = IntVar(master, 0)
knn_distance_algorithm = IntVar(master, 0)
municipality = StringVar(master)
address = StringVar(master)
room_number = StringVar(master)
square_footage = StringVar(master)
floor = StringVar(master)
elevator = IntVar()
balcony = IntVar()
registered = IntVar()
k = StringVar(master, "103")
prediction = Label(master, text="")


def print_vars():
    print(f"Municipality: {municipality.get()}")
    print(f": {address.get()}")
    print(f": {room_number.get()}")
    print(f": {square_footage.get()}")
    print(f": {floor.get()}")
    print(f": {elevator.get()}")
    print(f": {balcony.get()}")
    print(f": {registered.get()}")
    print(f": {algorithm.get()}")


def calculate_distance_from_center(municipality: str, address: str) -> float:
    bing_maps_key = "Ag2JbMXKFJqnkx9KFbScUGJ0szlyR7_BYzeo4ZfiEkfjr_SZMz24FOpVBImTndnk"

    wp0 = urllib.parse.quote(f"Beograd,{municipality}", safe='')
    wp1 = urllib.parse.quote(f"Beograd,{municipality},{address}", safe='')
    route_url = \
        f"http://dev.virtualearth.net/REST/v1/Routes/Walking?wp.0={wp0}&wp.1={wp1}&output=json&key={bing_maps_key}"

    try:
        request = urllib.request.Request(route_url)
        response = urllib.request.urlopen(request)
        result_str = response.read().decode(encoding="utf-8")
        result = json.loads(result_str)

        return result['resourceSets'][0]['resources'][0]['travelDistance']
    except BaseException as e:
        raise RuntimeError(f"Cannot calculate distance form municipality center. Error: {e}")


def predict():
    global algorithm, knn_distance_algorithm, municipality, address, room_number, square_footage, floor, elevator, \
        balcony, registered, k, prediction

    distance = calculate_distance_from_center(municipality.get(), address.get())

    x = np.array([[
        float(room_number.get()),
        float(square_footage.get()),
        int(floor.get()),
        elevator.get(),
        balcony.get(),
        registered.get(),
        distance
    ]])

    if algorithm.get() == 0:
        price = int(linear_regression_prediction(x)[0])
    else:
        price = knn_prediction(x, int(k.get()))

    prediction.config(text=f"{price} €")


if __name__ == '__main__':

    Radiobutton(master, text="Linear Regression", variable=algorithm, value=0, indicator=0,
                background="light blue", width=40, borderwidth=2).grid(row=0, column=0)
    Radiobutton(master, text="KNN", variable=algorithm, value=1, indicator=0,
                background="light blue", width=45, borderwidth=2).grid(row=0, column=1)

    Label(master, text="Municipality:").grid(row=1, column=0)
    Entry(master, textvariable=municipality, width=50, borderwidth=5).grid(row=1, column=1)

    Label(master, text="Address:").grid(row=2, column=0)
    Entry(master, textvariable=address, width=50, borderwidth=5).grid(row=2, column=1)

    Label(master, text="Room number:").grid(row=3, column=0)
    Entry(master, textvariable=room_number, width=50, borderwidth=5).grid(row=3, column=1)

    Label(master, text="Square footage (m^2):").grid(row=4, column=0)
    Entry(master, textvariable=square_footage, width=50, borderwidth=5).grid(row=4, column=1)

    Label(master, text="Floor:").grid(row=5, column=0)
    Entry(master, textvariable=floor, width=50, borderwidth=5).grid(row=5, column=1)

    Checkbutton(master, text="Elevator", variable=elevator).grid(row=6)
    Checkbutton(master, text="Balcony", variable=balcony).grid(row=7)
    Checkbutton(master, text="Registered", variable=registered).grid(row=8)

    Label(master, text="Parameters for KNN:").grid(row=9, column=0)

    Label(master, text="K:").grid(row=10, column=0)
    Entry(master, textvariable=k, width=50, borderwidth=5).grid(row=10, column=1)

    Radiobutton(master, text="Euclidean distance", variable=knn_distance_algorithm, value=0).grid(row=11, column=0)
    Radiobutton(master, text="Manhattan distance", variable=knn_distance_algorithm, value=1).grid(row=11, column=1)

    Label(master, text="Prediction:").grid(row=12, column=0)
    prediction.grid(row=12, column=1)

    Button(master, text="Predict price", command=predict).grid(row=13, column=1)

    master.mainloop()
