import controller_template as controller_template
import random
import math


class Controller(controller_template.Controller):
    def __init__(self, track, evaluate=True):
        super().__init__(track, evaluate=evaluate)

    def normaliza_feature(self, value, min, max):
        #if (mode): #normaliza entre [-1, 1]
        return (2 * (value - min)/(max - min)) - 1
        #else:
        #return (value - min)/(max - min) #normalize between [0, 1]



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
        f0,f1,f2,f3 = features[0], features[1], features[2], features[3]
        up = parameters[0] * f0 + parameters[1] * f1 + parameters[2] * f2 + parameters[3] * f3
        cair = parameters[4] * f0 + parameters[5] * f1 + parameters[6] * f2 + parameters[7] * f3

        if (up > cair):
        	return 1
        else:
        	return 2

    def compute_features(self, sensors):

        #normaliza todos valores
        water_UP = self.normaliza_feature(sensors[0], 1, 700)
        water_UP_RIGHT = self.normaliza_feature(sensors[1], 1, 700)
        obstacle_UP = self.normaliza_feature(sensors[2], 1, 700)
        obstacle_UP_RIGHT = self.normaliza_feature(sensors[3], 1, 700)
        obstacle_AHEAD = self.normaliza_feature(sensors[4], 1, 700)
        obstacle_DOWN_RIGHT = self.normaliza_feature(sensors[5], 1, 700)
        obstacle_DOWN = self.normaliza_feature(sensors[6], 1, 700)
        monster_UP = self.normaliza_feature(sensors[7], 1, 200)
        monster_UP_RIGHT = self.normaliza_feature(sensors[8], 1, 200)
        monster_AHEAD = self.normaliza_feature(sensors[9], 1, 200)
        monster_DOWN_RIGHT = self.normaliza_feature(sensors[10], 1, 200)
        monster_DOWN = self.normaliza_feature(sensors[11], 1, 200)
        oxygen = self.normaliza_feature(sensors[12], 1, 400)

        features_list = []
        # a = (1/(obstacle_AHEAD + 0.1)) #max 10 min 0.9090909091
        # b = (1/(obstacle_DOWN + 0.1))  #max 10 min 0.9090909091
        # c = (1/(obstacle_DOWN_RIGHT + 0.1))  #max 10 min 0.9090909091
        # d = (1/(monster_AHEAD + 0.1)) #max 10 min 0.9090909091
        # e = (1/(monster_DOWN + 0.1))
        # f = (1/(monster_DOWN_RIGHT + 0.1))
        # g = (1/(obstacle_UP + 0.1))
        # h = (1/(obstacle_UP_RIGHT + 0.1))
        # i = (1/(monster_UP + 0.1))
        # j = (1/(monster_UP_RIGHT + 0.1))
        # k = (1/(water_UP + 0.1))
        # l = (1/(water_UP_RIGHT + 0.1))

        f1 = (obstacle_AHEAD + obstacle_DOWN + (obstacle_DOWN_RIGHT)*2)
        f2 = ((monster_AHEAD)*2) + (monster_DOWN_RIGHT*2) + monster_UP_RIGHT
        f3 = (obstacle_UP + obstacle_DOWN)*2
        f4 = ((oxygen)*3) + ((water_UP)*2) + (water_UP_RIGHT * 2)

        f1 = self.normaliza_feature(f1, -1, 4)
        f2 = self.normaliza_feature(f2, -1, 5)
        f3 = self.normaliza_feature(f3, -1, 4)
        f4 = self.normaliza_feature(f4, -1, 7)

        features_list.append(f1)
        features_list.append(f2)
        features_list.append(f3)
        features_list.append(f4)
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
            #gera vizinhos de um estado
    def geraVizinhos(self,estado):
        perturbacao = 0.5
        vizinhos = []


        vi = estado[:]


        for j in range(len(vi)):
            perturbacao = random.uniform(-5,5)
            vi[j] += perturbacao

        return vi[:]

    def learn(self, weights):


        estado_atual = self.geraVizinhos([1,1,1,1,1,1,1,1])
        min_temperatura = 0
        T = 400
        while 1==1:

            T = T - 0.5
            print (T)
            if( T == min_temperatura):
                return estado_atual


            for i in range(1,30):
                estado_candidato = self.geraVizinhos(estado_atual)
                candidato = self.run_episode(estado_candidato)
                atual = self.run_episode(estado_atual)
                variacao_E =  candidato - atual

                print("Variação de E :",variacao_E)
                print("Valor do estado atual:", atual)
                print("Valor do estado candidato:", candidato)
                print("Estado Atual:", estado_atual)


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

                

        """
        HINT: you can call self.run_episode (see controller_template.py) to evaluate a given set of weights
        :param weights: initial weights of the controller (either loaded from a file or generated randomly)
        :return: the best weights found by your learning algorithm, after the learning process is over
        """
        #raise NotImplementedError("This Method Must Be Implemented")
