import random
import math
import matplotlib.pyplot as plt
from ciudades import Ciudad, leer_ciud, escrib_devolv, generar_ciudades, costo_rut


class Particula:
    def __init__(self, route, cost=None):
        self.route = route
        self.pbest = route
        self.current_cost = cost if cost else self.costo_rut()
        self.pbest_cost = cost if cost else self.costo_rut()
        self.velocity = []

    def velocidad(self):
        self.velocity.clear()

    def actualizar(self):
        self.current_cost = self.costo_rut()
        if self.current_cost < self.pbest_cost:
            self.pbest = self.route
            self.pbest_cost = self.current_cost

    def costo_rut(self):
        return costo_rut(self.route)


class Alg_pso:

    def __init__(self, iterations, population_size, gbest_probability=1.0, pbest_probability=1.0, ciudades=None):
        self.ciudades = ciudades
        self.gbest = None
        self.gcost_iter = []
        self.iterations = iterations
        self.population_size = population_size
        self.particles = []
        self.gbest_probability = gbest_probability
        self.pbest_probability = pbest_probability

        solutions = self.poblacion_inicial()
        self.particles = [Particula(route=solution) for solution in solutions]

    def random_rut(self):
        return random.sample(self.ciudades, len(self.ciudades))

    def poblacion_inicial(self):
        random_poblc = [self.random_rut() for _ in range(self.population_size - 1)]
        mejor_poblc = [self.mejor_rut(0)]
        return [*random_poblc, *mejor_poblc]
        # return [*random_population]

    def mejor_rut(self, start_index):
        unvisited = self.ciudades[:]
        del unvisited[start_index]
        route = [self.ciudades[start_index]]
        while len(unvisited):
            index, nearest_city = min(enumerate(unvisited), key=lambda item: item[1].distancia(route[-1]))
            route.append(nearest_city)
            del unvisited[index]
        return route

    def run(self):
        self.gbest = min(self.particles, key=lambda p: p.pbest_cost)
        print("\n\n\tAlgoritmo PSO del TSP con {} ciudades".format(len(self.ciudades)))
        plt.ion()
        plt.draw()

def ejec_pso():
    ciudades = leer_ciud()
    pso = Alg_pso(iterations=1200, population_size=300, pbest_probability=0.9, gbest_probability=0.02, ciudades=ciudades)
    pso.run()
    print('La mejor solucion obtenida del algorimo PSO es: %.4f' % pso.gbest.pbest_cost)

    x_list, y_list = [], []
    for ciudad in pso.gbest.pbest:
        x_list.append(ciudad.x)
        y_list.append(ciudad.y)

    x_list.append(pso.gbest.pbest[0].x)
    y_list.append(pso.gbest.pbest[0].y)
