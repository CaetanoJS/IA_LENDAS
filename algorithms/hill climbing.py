#funcao de aprendizado
    def hill_climbing(self, weights):

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
            ruido = 0.1
            #for each value of the state
            for i in range(list_size):
                rand_choice = random.randint(0, 1)
                if(rand_choice == 0):
                    list[i] -= ruido
                elif(rand_choice == 1):
                    list[i] += random.uniform(-3, 3)
            return list

        #define estado inicial como um estado aleatorio

        estado_atual = [random.uniform(-1, 1), random.uniform(-1, 1),random.uniform(-1, 1),
        random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1),
        random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]
        estado_atual = [0.9999999999999999, 0.20000000000000004, 0.20000000000000004, 0.7000000000000001, 0.4, 0.6, 0.4, 0.4, 0.20000000000000004, 0.20000000000000004, 0.9999999999999999, 0.4]

        while (1 == 1):
            v = geraVizinhos(estado_atual, 60)
            melhor_vizinho = estado_atual[:]
            for vizinhos in v:
                #testa os vizinhos do estado atual, indo sempre para o melhor vizinho
                print (melhor_vizinho)
                melhor_atual = self.run_episode(melhor_vizinho)
                vizinho_atual = self.run_episode(vizinhos)
                print ("melhor vizinho atual com valor: ", melhor_atual)
                print ("vizinho atual com valor: ", vizinho_atual)
                if (vizinho_atual > melhor_atual):
                    melhor_vizinho = vizinhos[:]
            #depois de passar por todos vizinhos, verifica se o melhor vizinho eh melhor
            #que o estado atual (inicial, definido como aleatorio)
            if (self.run_episode(melhor_vizinho) > self.run_episode(estado_atual)):
                print ("melhor vizinho final aqui ", melhor_vizinho)
                estado_atual = melhor_vizinho[:]
            else:
                print ("melhor vizinho eh o original ", estado_atual)
                pass
