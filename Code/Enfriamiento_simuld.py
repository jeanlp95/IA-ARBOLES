import math
import random
import matplotlib.pyplot as plt

class Sim_alg(object):
    def __init__(self, coords, T=-1, alpha=-1, stopping_T=-1, stopping_iter=-1):
        #Elementos
        self.coords = coords

        #Cantidad de elementos
        self.N = len(coords)

        #Temperatura minima
        self.T = math.sqrt(self.N) if T == -1 else T

        #Tasa de enfriamiento
        self.alpha = 0.995 if alpha == -1 else alpha
        self.stopping_temperature = 0.00000001 if stopping_T == -1 else stopping_T
        self.stopping_iter = 100000 if stopping_iter == -1 else stopping_iter
        self.iteration = 1

        """
        Inicializacion de la matriz de distancia
        Obtencion de los nodos
        Inicializacion de la solucion actual
        Inicializacion de
        """
        self.dist_matrix = self.matrix_dist(coords)
        self.nodes = [i for i in range(self.N)]

        self.cur_solution = self.sol_inc()
        self.best_solution = list(self.cur_solution)

        self.cur_fitness = self.vl_sol(self.cur_solution)
        print("\n\n\tAlgoritmo enfriamiento Simulado del TSP con {} ciudades".format(self.N))
        self.initial_fitness = self.cur_fitness
        self.best_fitness = self.cur_fitness

        self.fitness_list = [self.cur_fitness]
        self.T_list = [self.T]

    def sol_inc(self):
        """
        Algoritmo codicioso para obtener la solucion inicial
        """
        cur_node = random.choice(self.nodes)
        solution = [cur_node]

        free_list = list(self.nodes)
        random.shuffle(free_list)
        return free_list

    def dist(self, coord1, coord2):
        """
        Distancia euclidiana
        """
        return round(math.sqrt(math.pow(coord1[1] - coord2[1], 2) + math.pow(coord1[1] - coord2[1], 2)), 4)

    def matrix_dist(self, coords):
        n = len(coords)
        mat = [[self.dist(coords[i], coords[j]) for i in range(n)] for j in range(n)]
        return mat

    def vl_sol(self, sol):
        """ Valor objetivo de una solucion """
        return round(sum([self.dist_matrix[sol[i - 1]][sol[i]] for i in range(1, self.N)]) +
                     self.dist_matrix[sol[0]][sol[self.N - 1]], 4)

    def probabl_acept(self, candidate_fitness):
        """
        Probabilidad de aceptacion si el candidato es peor que el actual
        Depende de la temperatura actual y la diferencia entre el candidato y el actual
        """
        return math.exp(-abs(candidate_fitness - self.cur_fitness) / self.T)

    def acept_prob(self, candidate):
        """
        Acepta con probabilidad 1 si l candidado es mejor que el actual
        Acepta con probabilidad probabl_acept(...) si el candidato es peor
        """
        candidate_fitness = self.vl_sol(candidate)
        if candidate_fitness < self.cur_fitness:
            self.cur_fitness = candidate_fitness
            self.cur_solution = candidate
            if candidate_fitness < self.best_fitness:
                self.best_fitness = candidate_fitness
                self.best_solution = candidate
        else:
            if random.random() < self.probabl_acept(candidate_fitness):
                self.cur_fitness = candidate_fitness
                self.cur_solution = candidate

    def enfr_s(self):
        """
        Eejecutar el algoritmo de enfriamiento simulado
        """
        while self.T >= self.stopping_temperature and self.iteration < self.stopping_iter:
            candidate = list(self.cur_solution)
            l = random.randint(2, self.N - 1)
            i = random.randint(0, self.N - l)
            candidate[i:(i + l)] = reversed(candidate[i:(i + l)])
            self.acept_prob(candidate)
            self.T *= self.alpha
            self.iteration += 1
            self.fitness_list.append(self.cur_fitness)
            self.T_list.append(self.T)

        print('La mejor solucion obtenida del algoritmo enfriamiento simulado es: ', self.best_fitness)
        print('Temperatura: ', self.T)
