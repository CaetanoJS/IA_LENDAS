"""
Use this module to define the caves available in the game, or to create new ones.
"""
import cave as cave
from math import pi


##### CAVE0

cave0 = cave.Cave('assets/cave0.png', 'assets/cave0_textura.png', 'cave0')

cave0.episode_length = 1058 # [3300 - 125 (posição do centro do carro + largura a partir do centro) / 3 (velocidade do mapa de locomoção)], ou seja, é a quantidade de frames maximo que passa do inicio ate o fim do mapa
cave0.sub1_position = (100, 300)
cave0.sub2_position = (100, 90)
cave0.angle_of_subs = 2*pi
cave0.initial_oxygen = 400

#########

#### CAVE1

cave1 = cave.Cave('assets/cave1.png', 'assets/cave1_textura.png', 'cave1')

cave1.episode_length = 1058 # [3300 - 125 (posição do centro do carro + largura a partir do centro) / 3 (velocidade do mapa de locomoção)], ou seja, é a quantidade de frames maximo que passa do inicio ate o fim do mapa
cave1.sub1_position = (100, 300)
cave1.sub2_position = (100, 90)
cave1.angle_of_subs = 2*pi
cave1.initial_oxygen = 400


#########

##### CAVE2

cave2 = cave.Cave('assets/cave2.png', 'assets/cave2_textura.png', 'cave2')

cave2.episode_length = 1058 # [3300 - 125 (posição do centro do carro + largura a partir do centro) / 3 (velocidade do mapa de locomoção)], ou seja, é a quantidade de frames maximo que passa do inicio ate o fim do mapa
cave2.sub1_position = (100, 300)
cave2.sub2_position = (100, 90)
cave2.angle_of_subs = 2*pi
cave2.initial_oxygen = 400

#########

##### CAVE3

cave3 = cave.Cave('assets/cave3.png', 'assets/cave3_textura.png', 'cave3')

cave3.episode_length = 1058 # [3300 - 125 (posição do centro do carro + largura a partir do centro) / 3 (velocidade do mapa de locomoção)], ou seja, é a quantidade de frames maximo que passa do inicio ate o fim do mapa
cave3.sub1_position = (100, 300)
cave3.sub2_position = (100, 90)
cave3.angle_of_subs = 2*pi
cave3.initial_oxygen = 400

#########




