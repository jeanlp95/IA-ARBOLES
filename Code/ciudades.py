import math
import random
import matplotlib.pyplot as plt


class Ciudad:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distancia(self, ciudad):
        return math.hypot(self.x - ciudad.x, self.y - ciudad.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"


def leer_ciud():
    ciudades = []
    with open(f'data/data.txt', 'r') as handle:
        lines = handle.readlines()
        for line in lines:
            index = (line.index(',') + 1)
            x, y = map(float, line[index:].split(','))
            ciudades.append(Ciudad(x, y))
    return ciudades


def escrib_devolv(size):
    ciudades = generar_ciudades(size)
    with open(f'test_data/cities_{size}.data', 'w+') as handle:
        for ciudad in ciudades:
            handle.write(f'{ciudad.x} {ciudad.y}\n')
    return ciudades


def generar_ciudades(size):
    return [Ciudad(x=int(random.random() * 1000), y=int(random.random() * 1000)) for _ in range(size)]


def costo_rut(route):
    return sum([ciudad.distancia(route[index - 1]) for index, ciudad in enumerate(route)])


def visualizar_tsp(title, ciudades):
    fig = plt.figure()
    fig.suptitle(title)
    x_list, y_list = [], []
    for ciudad in ciudades:
        x_list.append(ciudad.x)
        y_list.append(ciudad.y)
    x_list.append(ciudades[0].x)
    y_list.append(ciudades[0].y)

    plt.plot(x_list, y_list, 'ro')
    plt.plot(x_list, y_list, 'g')
    plt.show(block=True)
