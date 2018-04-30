import random
#gera um estado inicial com os valores theta iniciais
def selecionaEstadoAleatorio(self, sensors):
    estado = []
    estado.append(0.5)
    estado.append(0.5)
    estado.append(0.5)
    return estado

#gera vizinhos de um estado
def geraVizinhos(estado, k):
    vizinhos = []
    for i in range(k):
        for j in range(k):
            new_weights = estado[i][:]
            disturbance = gera_ruido(new_weights)
            vizinhos.append(disturbance)
    return vizinhos

def gera_ruido(list):
    list_size = len(list)
    ruido = 0.1
    #for each value of the state
    for i in range(list_size):
        rand_choice = random.randint(0, 1)
        if(rand_choice == 0):
            list[i] -= ruido
        elif(rand_choice == 1):
            list[i] += ruido
    return list

#define estado inicial como um estado aleatorio

candidatos_iniciais = [[1, 1, 1, 1, 1, 1],[2, 2, 2, 2, 2, 2],[3, 3, 3, 3, 3, 3],[4, 4, 4, 4, 4, 4],[5, 5, 5, 5, 5, 5]]
candidatos_atuais = candidatos_iniciais[:]
k = 5

vizinhos = geraVizinhos(candidatos_atuais, k)
print (len(vizinhos))
