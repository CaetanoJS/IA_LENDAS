# -*- coding: utf-8 -*-
import math
import random
#######################Simulated Annealing#####################################

    #funcao de aprendizado do SA
def simulated_annealing(weights):
    #define estado inicial como um estado aleatorio
    estado_atual = weights
    min_temperatura = 1
    T = 100
    while 1==1:
        T = T - 0.2
        if( T == min_temperatura):
            return estado_atual
        for i in range(1,10):
            estado_candidato = geraVizinhos(estado_atual)
            variacao_E = self.run_episode(estado_candidato) - self.run_episode(estado_atual)
            if (variacao_E > 0):
                print("estado candidato é melhor que estado atual")
                estado_atual = estado_candidato
            else:
                value = math.exp(-variacao_E/T)
                verifica_prob = random.uniform(0,1)
                if(verifica_prob < value):
                    print("estado candidato é pior  que estado atual mas é escolhido pelo algoritimo de prob")
                    estado_atual = estado_candidato




def probabilidade_estado_candidato():
    value = math.exp(-variacao_E/T)
    return value


def geraVizinhos(estado):
    perturbacao = 0.5
    vizinhos = []


    vi = estado[:]
    perturbacao = random.uniform(-2,2)

    for j in range(len(vi)):
        vi[j] += perturbacao

    return vi



#################################################################################
