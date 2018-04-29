 import controller_template as controller_template
from random import randrange, uniform


class Controller(controller_template.Controller):
    def __init__(self, track, evaluate=True):
        super().__init__(track, evaluate=evaluate)



    #######################################################################
    ############## METHODS YOU NEED TO IMPLEMENT ##########################
    #######################################################################

    def take_action(self, parameters: list): #-> int:
        """
        :param parameters: Current weights/parameters of your controller

        :return: An integer corresponding to an action:
        1 - UP
        2 - NOTHING (GRAVITY)

        """
        features = self.compute_features(self.sensors)
        raise NotImplementedError("This Method Must Be Implemented")


    def compute_features(self, sensors):
        #inicialmente define 3 features aleatórias só para testar
        features_list = []
        f1 = sensors[0] + sensors[12] #tem agua acima e pouco oxigenio?
        f2 = sensors[2] - sensors [12] #tem monstro acima e bastante oxigenio?
        f3 = sensors[9] + sensors [2] #tem monstro a frente e ta livre pra ir pra cima?

        features_list.append(f1)
        features_list.append(f2)
        features_list.append(f3)
        return features_list

        """
        :sensors: List that contains (in order) the the following sensors (ranges of each sensor are also provided below)

        0	water_UP: 1-700
        1	water_UP_RIGHT: 1-700
        2    obstacle_UP: 1-700
        3	obstacle_UP_RIGHT: 1-700
        4	obstacle_AHEAD: 1-700
        5	obstacle_DOWN_RIGHT: 1-700
        6	obstacle_DOWN: 1-700
        7    monster_UP: 1-200
        8	monster_UP_RIGHT: 1-200
        9	monster_AHEAD: 1-200
        10	monster_DOWN_RIGHT: 1-200
        11	monster_DOWN: 1-200
        12	oxygen: 1-400

    """

    #gera um iterador infinito
    def inf(i=0, step=1):
        while True:
            yield i
            i+=step

    #gera um estado inicial com os valores theta iniciais
    def selecionaEstadoAleatorio(self, sensors):
        estado = []
        estado.append(0.5)
        estado.append(0.5)
        estado.append(0.5)
        return estado

    #gera vizinhos de um estado
    def geraVizinhos(self, estado):
        perturbacao = 0.1
        vizinhos = []

        for i in range(len(estado)):
            v1 = estado[:]
            v1[i] = estado[i] + perturbacao
            if (vizinhos.count(v1) < 1):
                vizinhos.append(v1)

            v1[i] = estado[i] - perturbacao
            if (vizinhos.count(v1) < 1):
                vizinhos.append(v1)

            for j in range(len(v2)):
                v2 = v1[:]
                if (j != i):
                    v2[j] = estado[j] + perturbacao
                    if (vizinhos.count(v2) < 1):
                        vizinhos.append(v2)

                    v2[j] = estado[j] - perturbacao
                    if (vizinhos.count(v2) < 1):
                        vizinhos.append(v2)

                for k in range(len(v2)):
                    v3 = v2[:]
                    if (j != k and j != i and k != j):
                        v3[k] = estado[k] + perturbacao
                        if (vizinhos.count(v1) < 1):
                            vizinhos.append(v3)
                        v3[k] = estado[k] - perturbacao
                        if (vizinhos.count(v1) < 1):
                            vizinhos.append(v3)
        return vizinhos


    #funcao de aprendizado
    def learn(self, weights):
        #define estado inicial como um estado aleatorio
        estado_atual = selecionaEstadoAleatorio()
        for i in inf():
            v = geraVizinhos(weights)
            melhor_vizinho = estado_atual
            for vizinhos in v:
                #testa os vizinhos do estado atual, indo sempre para o melhor vizinho
                if (self.run_episode(vizinhos) > self.run_episode(melhor_vizinho)):
                    melhor_vizinho = vizinhos
            #depois de passar por todos vizinhos, verifica se o melhor vizinho eh melhor
            #que o estado atual (inicial, definido como aleatorio)
            if (self.run_episode(melhor_vizinho) > self.run_episode(estado_atual)):
                return melhor_vizinho
            else:
                return estado_atual

        """
        HINT: you can call self.run_episode (see controller_template.py) to evaluate a given set of weights
        :param weights: initial weights of the controller (either loaded from a file or generated randomly)
        :return: the best weights found by your learning algorithm, after the learning process is over
        """
        #raise NotImplementedError("This Method Must Be Implemented")
