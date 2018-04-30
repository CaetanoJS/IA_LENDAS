import controller_template as controller_template
import random


class Controller(controller_template.Controller):
    def __init__(self, track, evaluate=True):
        super().__init__(track, evaluate=evaluate)

    def normaliza_feature(self, value, min, max):
        #if (mode): #normaliza entre [-1, 1]
        #return (2 * (value - min)/(max - min)) - 1
        #else:
        return (value - min)/(max - min) #normalize between [0, 1]



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
        up = parameters[0] * features[0] + parameters[1] * features[1] + parameters[2] * features[2]
        cair = parameters[3] * features[0] + parameters[4] * features[1] + parameters[5] * features[2]

        if (up > cair):
        	return 1
        else:
        	return 2

    def compute_features(self, sensors):

        #normaliza todos valores
        water_UP = self.normaliza_feature(sensors[0], 700, 1)
        water_UP_RIGHT = self.normaliza_feature(sensors[1], 700, 1)
        obstacle_UP = self.normaliza_feature(sensors[2], 700, 1)
        obstacle_UP_RIGHT = self.normaliza_feature(sensors[3], 700, 1)
        obstacle_AHEAD = self.normaliza_feature(sensors[4], 700, 1)
        obstacle_DOWN_RIGHT = self.normaliza_feature(sensors[5], 700, 1)
        obstacle_DOWN = self.normaliza_feature(sensors[6], 700, 1)
        monster_UP = self.normaliza_feature(sensors[7], 700, 1)
        monster_UP_RIGHT = self.normaliza_feature(sensors[8], 700, 1)
        monster_AHEAD = self.normaliza_feature(sensors[9], 700, 1)
        monster_DOWN_RIGHT = self.normaliza_feature(sensors[10], 700, 1)
        monster_DOWN = self.normaliza_feature(sensors[11], 700, 1)
        oxygen = self.normaliza_feature(sensors[12], 700, 1)



        #inicialmente define 3 features aleatórias só para testar
        features_list = []
        f1 = oxygen - water_UP
        f2 = obstacle_UP + monster_AHEAD
        f3 = obstacle_DOWN + obstacle_DOWN_RIGHT + monster_DOWN_RIGHT

        features_list.append(f1)
        features_list.append(f2)
        features_list.append(f3)
        return features_list

        """
        :sensors: List that contains (in order) the the following sensors (ranges of each sensor are also provided below)

        0	water_UP: 1-700
        1	water_UP_RIGHT: 1-700
        2   obstacle_UP: 1-700
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

    #funcao de aprendizado
    def learn(self, weights):
        #gera um estado inicial com os valores theta iniciais
        def selecionaEstadoAleatorio(self, sensors):
            estado = []
            estado.append(0.5)
            estado.append(0.5)
            estado.append(0.5)
            return estado


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
            ruido = 0.3
            #for each value of the state
            for i in range(list_size):
                rand_choice = random.randint(0, 1)
                if(rand_choice == 0):
                    list[i] -= ruido
                elif(rand_choice == 1):
                    list[i] += ruido
            return list

        #define estado inicial como um estado aleatorio

        estado_atual = [0.7, 0.7, 1.3, 1.3, 1.3, 0.7]
        while (1 == 1):
            v = geraVizinhos(estado_atual, 20)
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

        """
        HINT: you can call self.run_episode (see controller_template.py) to evaluate a given set of weights
        :param weights: initial weights of the controller (either loaded from a file or generated randomly)
        :return: the best weights found by your learning algorithm, after the learning process is over
        """
        #raise NotImplementedError("This Method Must Be Implemented")
