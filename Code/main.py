import Algoritm_genetico
import Algoritmo_pso
import Enfriamiento_simuld
import time

coords = []
with open('data/data.txt','r') as f:
    i = 0
    for line in f.readlines():
        line = [x.replace('\n','') for x in line.split(',')]
        coords.append([])
        for j in range(1,3):
            coords[i].append(float(line[j]))
        i += 1


if __name__ == "__main__":
    # ejecutando algoritmo genetico
    start_time = time.time()
    Algoritm_genetico.run()
    print('El tiempo de ejecucion del algoritmo genetico es: %.4f seg ' % (time.time() - start_time))

    # ejecutando Enfriamiento simulado
    start_time = time.time()
    Enfriamiento_simuld.Sim_alg(coords, stopping_iter = 150).enfr_s()
    print('El tiempo de ejecucion del algoritmo enfriamiento simulado es: %.4f seg ' % (time.time() - start_time))

    # ejecutando PSO
    start_time = time.time()
    Algoritmo_pso.ejec_pso()
    print('El tiempo de ejecucion del algoritmo PSO es: %.4f seg ' % (time.time() - start_time))
