#######################Simulated Annealing#####################################

    #funcao de aprendizado do SA
    def simulated_annealing(self, weights):
        #define estado inicial como um estado aleatorio
        estado_atual = selecionaEstadoAleatorio()
        for t in inf():
            T = decresce_temperatura(t)
            if( T == min_temperatura):
	        return estado_atual
            for i in range(1,max_vizinhos):
                estado_candidato = seleciona_vizinho_aleatorio(estado_atual)
	        variacao_E = self.run_episode(estado_candidato) - self.run_episode(estado_atual)
                if (variacao_E > 0):
                    estado_atual = estado_candidato
                else:
		    estado_atual = probabilidade_estado_candidato()#função que faz a probabilidade de um valor ser aceito

	def probabilidade_estado_candidato(self)
	    self.value = exp(-variação_E/T)
		return self.value

#################################################################################
