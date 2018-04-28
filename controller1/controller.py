import controller_template as controller_template
from random import randrange, uniform


class Controller(controller_template.Controller):
    def __init__(self, track, evaluate=True):
        super().__init__(track, evaluate=evaluate)



    #######################################################################
    ############## METHODS YOU NEED TO IMPLEMENT ##########################
    #######################################################################

    def take_action(self, parameters: list) -> int:
        """
        :param parameters: Current weights/parameters of your controller

        :return: An integer corresponding to an action:
        1 - UP
        2 - NOTHING (GRAVITY)

        """
        features = self.compute_features(self.sensors)
        raise NotImplementedError("This Method Must Be Implemented")

    def compute_features(self, sensors):
        """
        :sensors: List that contains (in order) the the following sensors (ranges of each sensor are also provided below)

	water_UP: 1-700
	water_UP_RIGHT: 1-700
    obstacle_UP: 1-700
	obstacle_UP_RIGHT: 1-700
	obstacle_AHEAD: 1-700
	obstacle_DOWN_RIGHT: 1-700
	obstacle_DOWN: 1-700
    monster_UP: 1-200
	monster_UP_RIGHT: 1-200
	monster_AHEAD: 1-200
	monster_DOWN_RIGHT: 1-200
	monster_DOWN: 1-200
	oxygen: 1-400

        """
        raise NotImplementedError("This Method Must Be Implemented")


    #gera um iterador infinito
    def inf(i=0, step=1):
        while True:
            yield i
            i+=step

    #gera um vetor de valores theta
    def selecionaEstadoAleatorio(self):
        estado = []
        #adiciona manualmente todos os valores
        estado.append(randrange(1, 700)) #water up
        estado.append(randrange(1, 700)) #water_UP_RIGHT
        estado.append(randrange(1, 700)) #obstacle_UP
        estado.append(randrange(1, 700)) #obstacle_UP_RIGHT
        estado.append(randrange(1, 700)) #obstacle_AHEAD
        estado.append(randrange(1, 700)) #obstacle_DOWN_RIGHT
        estado.append(randrange(1, 700)) #obstacle_DOWN
        estado.append(randrange(1, 200)) #monster_UP
        estado.append(randrange(1, 200)) #monster_UP_RIGHT
        estado.append(randrange(1, 200)) #monster_AHEAD
        estado.append(randrange(1, 200)) #monster_DOWN_RIGHT
        estado.append(randrange(1, 200)) #monster_DOWN
        estado.append(randrange(1, 400)) #oxygen
        return estado

    #gera vizinhos de um estado
    def geraVizinhos(self):
        



    #funcao de aprendizado
    def learn(self, weights):
        #define estado inicial como um estado aleatorio
        estado_atual = selecionaEstadoAleatorio()
        for i in inf():
            v = geraVizinhos()
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
