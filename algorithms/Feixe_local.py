
    #funcao de aprendizado
    def feixe_local(self, weights):
        #gera um estado inicial com os valores theta iniciais
        def geraCandidatosAleatorios(k):
            #gera um candidato aleatorio para a lista dos k candidatos
            def geraPesos(p):
                candidato = []
                for i in range(p):
                    candidato.append(random.randint(-100,100))
                return candidato
            #preenche a lista de k candidatos aleatorios
            candidatos = []
            for i in range(k):
                for j in range(len(weights)):
                    candidatos.append(geraPesos(len(weights)))
            return candidatos

        #gera vizinhos de um candidato
        def geraVizinhos(candidato, k):
            vizinhos = []
            for i in range(k):
                for j in range(k):
                    new_weights = candidato[i].copy()
                    disturbance = gera_ruido(new_weights)
                    vizinhos.append(disturbance)
            return vizinhos

        def gera_ruido(list):
            list_size = len(list)
            ruido = random.uniform(-5.0,5.0)
            ruido = round(ruido,2)
            #for each value of the state
            for i in range(list_size):
                rand_choice = random.randint(0, 1)
                if(rand_choice == 0):
                    list[i] -= ruido
                elif(rand_choice == 1):
                    list[i] += ruido
            return list

        #numero de candidatos e de vizinhos expandidos a partir de cada candidato
        k = 60
        #candidatos_atuais inicia com k candidatos aleatorios
        candidatos_atuais = geraCandidatosAleatorios(k)
        #candidatos_atuais = [[1.014, 0.363, 12.491, 19.156, 9.276, 9.828, -2.054, -2.314], [1.014, 0.363, 12.491, 19.156, 9.276, 9.828, -2.054, -2.314], [1.014, 0.363, 12.491, 19.156, 9.276, 9.828, -2.054, -2.314]]
        #k_melhores_atual vai armazenar uma lista com scores e o candidato que conseguiu cada score
        k_melhores_atual = [] # <<<<<<--------------- EH UMA LISTA DE TUPLAS (SCORE, CANDIDATO[])
        #vizinhos contem k^2 candidatos
        melhor_score = 0
        melhor_candidato = []

        while (1 == 1):

            vizinhos = geraVizinhos(candidatos_atuais, k)
            print ("Quantidade de vizinhos: ", len(vizinhos))
            #o for termina com os k melhores vizinhos da lista "vizinhos" e roda de novo a partir deles
            for v in vizinhos:
                score_atual = self.run_episode(v)
                if(score_atual > melhor_score):
                    melhor_score = score_atual
                    melhor_candidato = v[:]
                print ("score atual: ", score_atual)
                print ("melhor score: ", melhor_score)
                print ("pesos: ", melhor_candidato)

                if(len(k_melhores_atual) < k):
                    k_melhores_atual.append([score_atual,v])
                else:
                    #decide se vai entrar ou nao na lista dos k_melhores do momento
                    for i in range(k):
                            if(k_melhores_atual[i][0] < score_atual):
                                k_melhores_atual[i] = [score_atual,v]
                                break

            print ("--------------------------------")
            for i in range(len(k_melhores_atual)):
                vizinhos[i] = k_melhores_atual[i][1]
            print ("melhor score: ", melhor_score)
            print ("melhor candidato: ", melhor_candidato)
            print ("--------------------------------")
            pass

        #raise NotImplementedError("This Method Must Be Implemented")
