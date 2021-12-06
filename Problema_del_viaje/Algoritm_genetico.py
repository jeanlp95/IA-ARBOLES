from sys import maxsize
from time import time
from random import random, randint, sample, seed
from haversine import haversine
import argparse
from datetime import datetime
import pandas as pd
import math

class Gene:  # Ciudad
    # Contiene distancias de ciudades
    __distances_table = {}

    def __init__(self, name, lat, lng):
        self.name = name
        self.lat = lat
        self.lng = lng

    def obtener_dist(self, dest):
        return round(math.sqrt(math.pow(self.lat - dest.lat, 2) + math.pow(self.lng - dest.lng, 2)), 4)


class Individual:  # Ruta: posible solucion a el problema del viajero
    def __init__(self, genes):
        assert(len(genes) > 3)
        self.genes = genes
        self.__reset_params()

    def swap(self, gene_1, gene_2):
        self.genes[0]
        a, b = self.genes.index(gene_1), self.genes.index(gene_2)
        self.genes[b], self.genes[a] = self.genes[a], self.genes[b]
        self.__reset_params()

    def add(self, gene):
        self.genes.append(gene)
        self.__reset_params()

    @property
    def fitness(self):
        if self.__fitness == 0:
            self.__fitness = 1 / self.travel_cost  # Normalizar el costo del recorrido
        return self.__fitness

    @property
    def travel_cost(self):  #Obtener el costo total del recorrido
        if self.__travel_cost == 0:
            for i in range(len(self.genes)):
                origin = self.genes[i]
                if i == len(self.genes) - 1:
                    dest = self.genes[0]
                else:
                    dest = self.genes[i+1]

                self.__travel_cost += origin.obtener_dist(dest)

        return self.__travel_cost

    def __reset_params(self):
        self.__travel_cost = 0
        self.__fitness = 0


class Poblacion:  # Poblacion de individuos
    def __init__(self, individuals):
        self.individuals = individuals

    @staticmethod
    def gen_individuals(sz, genes):
        individuals = []
        for _ in range(sz):
            individuals.append(Individual(sample(genes, len(genes))))
        return Poblacion(individuals)

    def add(self, route):
        self.individuals.append(route)

    def rmv(self, route):
        self.individuals.remove(route)

    def get_fittest(self):
        fittest = self.individuals[0]
        for route in self.individuals:
            if route.fitness > fittest.fitness:
                fittest = route

        return fittest


def evolve(pop, tourn_size, mut_rate):
    new_generation = Poblacion([])
    pop_size = len(pop.individuals)
    elitism_num = pop_size // 2

    # Elitismo
    for _ in range(elitism_num):
        fittest = pop.get_fittest()
        new_generation.add(fittest)
        pop.rmv(fittest)

    # Cruce
    for _ in range(elitism_num, pop_size):
        parent_1 = selection(new_generation, tourn_size)
        parent_2 = selection(new_generation, tourn_size)
        child = crossover(parent_1, parent_2)
        new_generation.add(child)

    # Mutacion
    for i in range(elitism_num, pop_size):
        mutate(new_generation.individuals[i], mut_rate)

    return new_generation


def crossover(parent_1, parent_2): #Cruce
    def fill_with_parent1_genes(child, parent, genes_n):
        start_at = randint(0, len(parent.genes)-genes_n-1)
        finish_at = start_at + genes_n
        for i in range(start_at, finish_at):
            child.genes[i] = parent_1.genes[i]

    def fill_with_parent2_genes(child, parent):
        j = 0
        for i in range(0, len(parent.genes)):
            if child.genes[i] == None:
                while parent.genes[j] in child.genes:
                    j += 1
                child.genes[i] = parent.genes[j]
                j += 1

    genes_n = len(parent_1.genes)
    child = Individual([None for _ in range(genes_n)])
    fill_with_parent1_genes(child, parent_1, genes_n // 2)
    fill_with_parent2_genes(child, parent_2)

    return child


def mutate(individual, rate): #Mutacion
    for _ in range(len(individual.genes)):
        if random() < rate:
            sel_genes = sample(individual.genes, 2)
            individual.swap(sel_genes[0], sel_genes[1])


def selection(poblacion, competitors_n): #Seleccion
    return Poblacion(sample(poblacion.individuals, competitors_n)).get_fittest()


def run_ga(genes, pop_size, n_gen, tourn_size, mut_rate, verbose=1):
    poblacion = Poblacion.gen_individuals(pop_size, genes)
    history = {'costo': [poblacion.get_fittest().travel_cost]}
    counter, generations, min_cost = 0, 0, maxsize

    if verbose:
        print("Ejecutanto algoritmo genetico...")

    start_time = time()
    while counter < n_gen:
        poblacion = evolve(poblacion, tourn_size, mut_rate)
        cost = poblacion.get_fittest().travel_cost

        if cost < min_cost:
            counter, min_cost = 0, cost
        else:
            counter += 1

        generations += 1
        history['costo'].append(cost)

    total_time = round(time() - start_time, 6)

    if verbose:
        print("Evolucion finalizada despues de {} generaciones".format(generations))
        print("El costo minimo del Altgorimo Genetico: {}".format(min_cost))

    history['generaciones'] = generations
    history['tiempo_total'] = total_time
    history['ruta'] = poblacion.get_fittest()

    return history

def load_genes(fn, sample_n=0):
    df = pd.read_csv(fn)
    genes = [Gene(row[0], row[1], row[2])
             for _, row in df.iterrows()]

    return genes if sample_n <= 0 else sample(genes, sample_n)

def run():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', type=int, default=1)
    parser.add_argument('--pop_size', type=int, default=500, help='Population size')
    parser.add_argument('--tourn_size', type=int, default=50, help='Tournament size')
    parser.add_argument('--mut_rate', type=float, default=0.02, help='Mutation rate')
    parser.add_argument('--n_gen', type=int, default=20, help='Número de generaciones iguales antes de detenerse')
    parser.add_argument(
        '--cities_fn',
        type=str,
        default="data/data.txt",
        help='Datos que contienen las coordenadas geográficas de las ciudades.'
    )

    seed(datetime.now())
    args = parser.parse_args()

    if args.tourn_size > args.pop_size:
        raise argparse.ArgumentTypeError('El tamaño del tourn_size no puede ser mayor que el tamaño de la población.')

    genes = load_genes(args.cities_fn)

    if args.verbose:
        print("\tAlgoritmo Genetico del TSP con {} ciudades".format(len(genes) + 1))

    history = run_ga(
        genes,
        args.pop_size,
        args.n_gen,
        args.tourn_size,
        args.mut_rate,
        args.verbose
    )

    if args.verbose:
        print("Algoritmo Genetico Finalizado")
