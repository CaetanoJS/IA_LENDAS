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
        f0,f1,f2,f3 = features[0], features[1], features[2], features[3]
        up = parameters[0] * f0 + parameters[1] * f1 + parameters[2] * f2 + parameters[3] * f3
        cair = parameters[4] * f0 + parameters[5] * f1 + parameters[6] * f2 + parameters[7] * f3

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
        a = (1/(obstacle_AHEAD + 0.1))
        b = (1/(obstacle_DOWN + 0.1))
        c = (1/(obstacle_DOWN_RIGHT + 0.1))
        d = (1/(monster_AHEAD + 0.1))
        e = (1/(monster_DOWN + 0.1))
        f = (1/(monster_DOWN_RIGHT + 0.1))
        g = (1/(obstacle_UP + 0.1))
        h = (1/(obstacle_UP_RIGHT + 0.1))
        i = (1/(monster_UP + 0.1))
        j = (1/(monster_UP_RIGHT + 0.1))

        f1 = ((water_UP/(oxygen + 0.1))) + (1/(water_UP+0.1)) + (1/(water_UP_RIGHT+0.1))
        f2 = (a + b + c)


        f3 = (d + e + f)

        f4 = i + j + g + h


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

    #funcao de aprendizado
    def learn(self, weights):
        #gera um estado inicial com os valores theta iniciais
        def geraCandidatosAleatorios(k):
            #gera um candidato aleatorio para a lista dos k candidatos
            def geraPesos(p):
                candidato = []
                for i in range(p):
                    candidato.append(random.randint(0,10))
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
            ruido = 0.3
            #for each value of the state
            for i in range(list_size):
                rand_choice = random.randint(0, 1)
                if(rand_choice == 0):
                    list[i] -= ruido
                elif(rand_choice == 1):
                    list[i] += ruido
            return list


        #numero de candidatos e de vizinhos expandidos a partir de cada candidato
        k = 3
        #candidatos_atuais inicia com k candidatos aleatorios
        #candidatos_atuais = geraCandidatosAleatorios(k)
        candidatos_atuais = [[1.014, 0.363, 12.491, 19.156, 9.276, 9.828, -2.054, -2.314], [1.014, 0.363, 12.491, 19.156, 9.276, 9.828, -2.054, -2.314], [1.014, 0.363, 12.491, 19.156, 9.276, 9.828, -2.054, -2.314]]
        #k_melhores_atual vai armazenar uma lista com scores e o candidato que conseguiu cada score
        k_melhores_atual = [] # <<<<<<--------------- EH UMA LISTA DE TUPLAS (SCORE, CANDIDATO[])
        #vizinhos contem k^2 candidatos
        vizinhos = geraVizinhos(candidatos_atuais, k)
        melhor_score = 0
        print (len(vizinhos))
        while (1 == 1):
            #o for termina com os k melhores vizinhos da lista "vizinhos" e roda de novo a partir deles
            for v in vizinhos:
                score_atual = self.run_episode(v)
                if(melhor_score < score_atual):
                    melhor_score = score_atual
                    melhor_candidato = v[:]
                print ("score atual: ", score_atual)
                print ("melhor score: ", melhor_score)
                #decide se vai entrar ou nao na lista dos k_melhores do momento
                for i in range(k):
                    if(len(k_melhores_atual) < k):
                        k_melhores_atual.append([score_atual,v])
                    else:
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
