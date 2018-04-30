import random


#gera vizinhos aleatórios de um estado
estado = [1,2]
def geraVizinhos(estado):
    perturbacao = 0.5
    vizinhos = []

    for v in range(0,10):
        vi = estado[:]
        perturbacao = random.uniform(-1,1)

        for j in range(len(vi)):
            vi[j] += perturbacao

        if vi not in vizinhos:
            vizinhos.append(vi)

    print(vizinhos)


geraVizinhos(estado)
            