# -*- coding: utf-8 -*-
import random


#gera vizinhos aleatórios de um estado
estado = [1,2]
def geraVizinhos(estado):
    perturbacao = 0.5
    vizinhos = []

    
    vi = estado[:]
    perturbacao = random.uniform(-2,2)

    for j in range(len(vi)):
        vi[j] += perturbacao

    return vi

value = geraVizinhos(estado)
print (value)     