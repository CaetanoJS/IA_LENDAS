import random
#from math import floor


#gera vizinhos de um estado
def geraVizinhos(estado, numVizinhos):
    vizinhos = []
    for i in range(numVizinhos):
        new_weights = estado[:]
        disturbance = gera_ruido(new_weights)
        vizinhos.append(disturbance) 
    return vizinhos

def gera_ruido(list):
    list_size = len(list)
    ruido = 0.5

    #for each value of the state
    for i in range(list_size):
        rand_choice = random.randint(0, 1)
        print(rand_choice)
        if(rand_choice == 0):
        	list[i] -= ruido 
        elif(rand_choice == 1):
        	list[i] += ruido	            
    return list  

li = [3, 5, 6, 4]
li = geraVizinhos(li,10)
print(li)