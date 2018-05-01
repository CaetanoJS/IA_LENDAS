    def Simulated_Annealing(self, weights):


            #gera vizinhos de um estado
        def geraVizinhos(estado):
            perturbacao = 0.5
            vizinhos = []


            vi = estado[:]


            for j in range(len(vi)):
                perturbacao = random.uniform(-1,1)
                vi[j] += perturbacao

            return vi

        estado_atual = [5,2,1,3,2,1]
        min_temperatura = 0
        T = 200
        while 1==1:

            T = T - 1
            print (T)
            if( T == min_temperatura):
                return estado_atual


            for i in range(1,20):
                estado_candidato = geraVizinhos(estado_atual)
                candidato = self.run_episode(estado_candidato)
                atual = self.run_episode(estado_atual)
                variacao_E =  candidato - atual

                print("Variação de E :",variacao_E)

                if (variacao_E > 0):
                    print("Variação positiva")
                    estado_atual = estado_candidato[:]

                elif(variacao_E < 0):
                    value = math.exp(variacao_E/T)
                    verifica_prob = random.uniform(0,1)

                    print("variação negativa")
                    print("verifica prob:", verifica_prob)
                    print('Função de prob: %.10f' % value)

                    if(verifica_prob < value):
                        print("Acertou probabilidade")
                        estado_atual = estado_candidato[:]


a = geraVizinhos[1,1,1,1,1]
print(a)