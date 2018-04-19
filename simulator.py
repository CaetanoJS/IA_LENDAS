"""
This is the Simulator module. All sensors variables and physics handling are implemented here. You don't need to read this
code to understand this assignment. If you came here because of a bug, please let us know about it.

Attributes:
    int width,height: size of window and simulation space. Changing these variable may cause unexpected behaviour!
    bool evaluate: If GUI will be rendered or not.
"""
import math
import random
import sys

import numpy as np
import pygame
from PIL import Image
from pygame.color import THECOLORS

import pymunk as pymunk
from pymunk import Vec2d
from pymunk.pygame_util import draw
from trigonometry import *

# PyGame screen dimensions
width = 1000
height = 700

#Background size
bwidth = 3300

# Gui Flag
evaluate = True

# Colision types required by pumunk
SUB_COLLISION_TYPE = 500

#Oxigenio maximo
MAX_OXYGEN = 400

#oxigenio atribuido quando o submarino estiver na agua
ADD_OXYGEN = 4

LOST_OXYGEN = 1

INITIAL_OXYGEN = 100

#VELOCIDADE DE LOCOMOÇAO DO MAPA
MAP_SPEED = 3

#images to be used
sub_image = "assets/sub.png"
sub2_image = "assets/sub2.png"


def block_print():
    """
    Disables print because I know you didn't compile chipmunk to disable debugs warnings
    """
    sys.stdout = None


def enable_print():
    sys.stdout = sys.__stdout__

def get_point_from_rgb_list(x: int, y: int, image_vector: 'list of rgb elements') -> list:
    """
    Get point from pygame rgb vector using pymunk coordinates
    :param x: pymunk x coordinate
    :param y: pymunk y coordinate
    :param image_vector: pygame Image

    :return: an list that contain a rgb vector
    """
    #height - y cuz its inverse for pymunk
    pos = (height - y) * bwidth + x
    try:
        return image_vector[pos]
    except IndexError:
        return image_vector[0]


class Background(pygame.sprite.Sprite):
    def __init__(self, image_path: str, location: (int, int)):
        """
        # Simple class extension to make easier to draw background

        :param image_path:
        :param location:
        """
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (bwidth, 700))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        #bgx = onde começa a coordenada x da tela a ser printada
        self.bgx = 0
        #bgspeed = velocidade de locomoção da tela
        self.bgspeed = MAP_SPEED
        pass
    
    #printa a imagem bgx pixels para a esquerda
    def render(self, screen):
        screen.fill(THECOLORS["black"])
        screen.blit(self.image, (self.bgx, 0))
    
    #bgx é incrementado para o próximo print da tela e, consequentemente, locomoção desta
    def update(self):
        self.bgx -= self.bgspeed
        pass

    def reset(self):
        self.bgx = 0
        pass

    @property
    def bgxvalue(self) -> int:
        return self.bgx

class SubShape(pymunk.Poly):
    def __init__(self, body, rectangle, sub_bound):
        """
        Simple extension of Pymunk's Poly class

        :param body: Pymunk body object
        :param rectangle: Polygon coordinates forming and rectangle
        :param sub_bound: s object which shape is beeing linked to.
        """
        self.class_bound = sub_bound
        super().__init__(body, rectangle)
        pass


class _Sub:
    def __init__(self, space, track, position, initial_oxygen, track_rgb, off_track_color,
                 img_path, global_track, water_color, octopus_color, screen=None):
        """
        This class is used to represent a Sub in the Simulation, it handles movement and sensors.

        :param space: pymunk space
        :param track: Track object which contains
        :param position: tuple containing x,y coordinates
        :param initial_oxygen: initial oxygen varies for each cave
        :param track_rgb: rgb vector containing track information
        :param off_track_color: collor that represent off_track in track_rgb
        :param img_path: path of the image
        :param global_track: background information
        :param water_color: water rgb
        :param octopus_color: octopus rgb
        :param screen: Pymunk screen
        """

        # Initializing class variables
	
        self.sub_img_shape = pygame.image.load(img_path)
        self.position = position
        self.space = space
        self.track = track
        self.off_track_color = off_track_color
        self.track_rgb = track_rgb
        self._create_new_sub_body()
        self.point_in_front = 0
        self.sub_direction = Vec2d(0,0)
        self.on_track = True
        self.frame_count = 0
        self.first = True
        self.octopus_on = False
        self.initial_oxygen = initial_oxygen
        self.global_track = global_track
        self.water_color = water_color
        self.octopus_color = octopus_color
        self.oxygen = self.initial_oxygen
        self.octopus_view = 0

        # Creates screen instance if in evaluate mode
        if evaluate:
            self.screen = screen

    def sub_step(self, action: int):

        """
        Prepare sub for next frame

        :param action: Integer indicating sub's action
        """

        self.frame_count += 1

        self.bgx = self.global_track.bgxvalue

        # Turning actions
        # Verifies if sub is getting hugged by the octopus, if so sub cant move
        if action == 1 and self.octopus_on == False:  # Turn right. CIMA
            driving_direction = Vec2d(0,1)
            vel = 400
        elif self.octopus_on == False:
            driving_direction = Vec2d(0,-1)
            vel = 20
        else:
            driving_direction = Vec2d(0,0)
            vel = 0

        self.t_x, self.t_y = self.sub_body.position

        #verifica se o box do submarino tá na posição andável
        self.on_track = True
        if (self.t_y + 10) >= height or (self.t_y - 15) <= 0:
            self.on_track = False
        else:
            for w1 in range(-25, 25):
                if get_point_from_rgb_list(int(int(self.t_x) - self.bgx + w1), int(self.t_y - 15), self.track_rgb) == self.off_track_color:
                    self.on_track = False
                elif get_point_from_rgb_list(int(int(self.t_x) - self.bgx + w1), int(self.t_y + 10), self.track_rgb) == self.off_track_color:
                    self.on_track = False
            for h1 in range(-15, 10):
                if get_point_from_rgb_list(int(int(self.t_x) - self.bgx - 25), int(self.t_y + h1), self.track_rgb) == self.off_track_color:
                            self.on_track = False
                elif get_point_from_rgb_list(int(int(self.t_x) - self.bgx + 25), int(self.t_y + h1), self.track_rgb) == self.off_track_color:
                            self.on_track = False


        #verifica se o sub colidiu com o octopus
        self.octopus_on = False
        for w1 in range(-25, 25):
            if get_point_from_rgb_list(int(int(self.t_x) - self.bgx + w1), int(self.t_y - 15), self.track_rgb) == self.octopus_color:
                    self.octopus_on = True
            elif get_point_from_rgb_list(int(int(self.t_x) - self.bgx + w1), int(self.t_y + 10), self.track_rgb) == self.octopus_color:
                    self.octopus_on = True
        for h1 in range(-15, 10):
            if get_point_from_rgb_list(int(int(self.t_x) - self.bgx - 25), int(self.t_y + h1), self.track_rgb) == self.octopus_color:
                    self.octopus_on = True
            elif get_point_from_rgb_list(int(int(self.t_x) - self.bgx + 25), int(self.t_y + h1), self.track_rgb) == self.octopus_color:
                    self.octopus_on = True

        # Updates sub velocity vector
        self.sub_body.velocity = vel * driving_direction

        # Updates sub angle
        self.sub_direction = driving_direction

	# CHECA SE TÁ NA ÁGUA
        if get_point_from_rgb_list(int(int(self.t_x) - self.bgx), int(self.t_y), self.track_rgb) == self.water_color:
            #adiciona apenas oxigenio suficiente para não ultrapassar o máximo
            if (MAX_OXYGEN - self.oxygen) < ADD_OXYGEN:
                self.oxygen += (MAX_OXYGEN - self.oxygen)
            else:
                self.oxygen += ADD_OXYGEN
        elif self.octopus_on == False:
            self.oxygen -= LOST_OXYGEN
        else:
            self.oxygen -= LOST_OXYGEN * 2

        self.sub_body.apply_impulse(self.sub_direction)
        pass

    def draw(self):
        """
        Draws sub on screen according velocity
        """
        if evaluate:
            p = self.sub_body.position
            # Correct p because pygame crazy coordinate system
            p = Vec2d(p.x, height - p.y)

            # Transform image to right size and flips it
            new_img = pygame.transform.scale(self.sub_img_shape, (50, 30))

            # Rotates image and place it at subs position
            offset = Vec2d(new_img.get_size()) / 2.
            p = p - offset

            # Renders Image
            self.screen.blit(new_img, p)

            # render oxygen
            pygame.draw.rect(self.screen, (255, 255, 255), [60,685,self.oxygen,10])


    def _create_new_sub_body(self):
        """
        Setups a bunch of pymunk's configurations
        """
        rectangle = [(-25, -15), (-25, 10), (25, 10), (25, -15)]
        self.sub_body = pymunk.Body(100, pymunk.inf)
        self.sub_body.position = self.position[0], self.position[1]
        self.sub_shape = SubShape(self.sub_body, rectangle, self)
        self.sub_shape.color = (51, 51, 0, 51)
        self.sub_shape.elasticity = 0
        self.sub_body.angle = self.track.angle_of_subs
        self.sub_shape.collision_type = SUB_COLLISION_TYPE
        driving_direction = Vec2d(0,-1)
        self.sub_body.apply_impulse(driving_direction)
        self.space.add(self.sub_body, self.sub_shape)


    def _draw_track_sensor(self, rotated_p: (float, float)):
        """
        Draws an obstacle sensor
        :param rotated_p: The point where the sensor has ended
        """
        if evaluate:
            pygame.draw.line(self.screen, (255, 255, 255), rotated_p,
                             (self.sub_body.position[0], height - self.sub_body.position[1]))

    def _draw_oct_sensor(self, rotated_p: (float, float)):
        """
        Draws an octopus sensor
        :param rotated_p: The point where the sensor has ended
        """
        if evaluate:
            pygame.draw.line(self.screen, (255, 0, 0), rotated_p,
                             (self.sub_body.position[0], height - self.sub_body.position[1]))

    def _draw_water_track_sensor(self, rotated_p: (float, float)):
        """
        Draws a water sensor
        :param rotated_p: The point where the sensor has ended
        """
        if evaluate:
            pygame.draw.line(self.screen, (0, 0, 255), rotated_p,
                             (self.sub_body.position[0], height - self.sub_body.position[1]))

    def reset(self):
        """
        Reset sub variables to prepare for another simulation
        """
        self.first = True
        self.frame_count = 0
        self.oxygen = self.initial_oxygen
        self.on_track = True
        self.space.remove(self.sub_body, self.sub_shape)
        self._create_new_sub_body()

    @property
    def sensors(self) -> list:

        """
        :return: List which contains (in order):

	distancia-agua cima: 1-700
	distancia-agua centro-cima 45graus: 1-700
        distancia obstaculos cima: 1-700
	distancia obstaculos centro-cima 45 graus: 1-700
	distancia obstaculos centro: 1-700
	distancia obstaculos centro-baixo 45 graus: 1-700
	distancia obstaculos baixo: 1-700
        distancia polvo cima: 1-200
	distancia polvo centro-cima 45 graus: 1-200
	distancia polvo centro: 1-200
	distancia polvo centro-baixo 45 graus: 1-200
	distancia polvo baixo: 1-200
	oxigenio: 1-400

        
        """

        # Default values
        self.obstacle_distance = -1
        self.obstacle_body_position_angle = 0

        # Gets track readings
        x, y = self.sub_body.position
        readings = self._get_sonar_readings(x, y, self.sub_body.angle)
        
        # antenas
        sensors = [readings[0], readings[1], readings[2], readings[3], readings[4], readings[5], readings[6], readings[7], readings[8], readings[9], readings[10], readings[11], self.oxygen]

        return sensors

    def _get_sonar_readings(self, x: float, y: float, angle):
        """
        Get track readings given sub position and angle
        :param x: sub x
        :param y: sub y
        :param angle: sub angle

        :return: list
        """

        readings = []
        # Make our arms.
        arm_left = self.make_sonar_arm(x, y)
        arm_middle = arm_left
        arm_right = arm_left
        arm_top = arm_left
        arm_bottom = arm_left

        arm_water_top = self.make_water_arm(x,y)
        arm_water_left = arm_water_top

        arm_octopus_left = self.make_octopus_arm(x,y)
        arm_octopus_middle = arm_octopus_left
        arm_octopus_right = arm_octopus_left
        arm_octopus_top = arm_octopus_left
        arm_octopus_bottom = arm_octopus_left

        # Rotate them and get readings.
        # water
        readings.append(self._get_water_distance(arm_water_top, x, y, angle, 1.57))
        readings.append(self._get_water_distance(arm_water_left, x, y, angle, 0.75))
        # obstacles
        readings.append(self._get_arm_distance(arm_top, x, y, angle, 1.57))
        readings.append(self._get_arm_distance(arm_left, x, y, angle, 0.75))
        readings.append(self._get_arm_distance(arm_middle, x, y, angle, 0, center=True))
        readings.append(self._get_arm_distance(arm_right, x, y, angle, -0.75))
        readings.append(self._get_arm_distance(arm_bottom, x, y, angle, -1.57))
        # octopus
        readings.append(self._get_octopus_distance(arm_octopus_top, x, y, angle, 1.57))
        readings.append(self._get_octopus_distance(arm_octopus_left, x, y, angle, 0.75))
        readings.append(self._get_octopus_distance(arm_octopus_middle, x, y, angle, 0, center=True))
        readings.append(self._get_octopus_distance(arm_octopus_right, x, y, angle, -0.75))
        readings.append(self._get_octopus_distance(arm_octopus_bottom, x, y, angle, -1.57))

        if evaluate:
            pygame.display.update()

        return readings

    def _get_arm_distance(self, arm: list, x: float, y: float, angle: float, offset: float, center=False) -> int:
        # Used to count the distance.
        """
        Calculates track sensor values
        :param arm: sonar arm
        :param x: sub x
        :param y: sub y
        :param angle: sub angle
        :param offset: used for correction
        :param center: True if this is the central track sensor, false otherwise

        :return: Distance ranging from 1-100
        """
        i = 0
        rotated_p = (0, 0)

        # Look at each point and see if we've hit something.

        for point in arm:
            i += 1

            # Move the point to the right spot.
            rotated_p = self.get_rotated_point(
                x, y, point[0], point[1], angle + offset
            )
            if i == 1 and center:
                self.point_in_front = rotated_p

            # Check if we've hit something. Return the current i (distance)
            # if we did.
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= width or rotated_p[1] >= height:
                self._draw_track_sensor(rotated_p)
                return 700  # Sensor is off the screen. return max distance
            else:
                obs = get_point_from_rgb_list((rotated_p[0] - self.bgx), height - rotated_p[1], self.track_rgb)
                if self.get_track_or_not(obs) != 0:
                    self._draw_track_sensor(rotated_p)
                    return i

        self._draw_track_sensor(rotated_p)
        return i

    def _get_octopus_distance(self, arm: list, x: float, y: float, angle: float, offset: float, center=False) -> int:
        # Used to count the distance.
        """
        Calculates track sensor values
        :param arm: sonar arm
        :param x: sub x
        :param y: sub y
        :param angle: sub angle
        :param offset: used for correction
        :param center: True if this is the central track sensor, false otherwise
        :return: Distance ranging from 1-100
        """
        i = 0
        rotated_p = (0, 0)

        # Look at each point and see if we've hit something.

        for point in arm:
            i += 1

            # Move the point to the right spot.
            rotated_p = self.get_rotated_point(
                x, y, point[0], point[1], angle + offset
            )
            if i == 1 and center:
                self.point_in_front = rotated_p

            # Check if we've hit something. Return the current i (distance)
            # if we did.
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= width or rotated_p[1] >= height:
                self._draw_oct_sensor(rotated_p)
                return 200  # Sensor is off the screen. return max distance
            else:
                obs = get_point_from_rgb_list((rotated_p[0] - self.bgx), height - rotated_p[1], self.track_rgb)
                if self.get_octopus_or_not(obs) != 0:
                    self._draw_oct_sensor(rotated_p)
                    return i

        self._draw_oct_sensor(rotated_p)
        return i

    def _get_water_distance(self, arm: list, x: float, y: float, angle: float, offset: float, center=False) -> int:
        # Used to count the distance.
        """
        Calculates track sensor values
        :param arm: sonar arm
        :param x: sub x
        :param y: sub y
        :param angle: sub angle
        :param offset: used for correction
        :param center: True if this is the central track sensor, false otherwise
        :return: Distance ranging from 1-100
        """
        i = 0
        rotated_p = (0, 0)

        # Look at each point and see if we've hit something.

        for point in arm:
            i += 1

            # Move the point to the right spot.
            rotated_p = self.get_rotated_point(
                x, y, point[0], point[1], angle + offset
            )
            if i == 1 and center:
                self.point_in_front = rotated_p

            # Check if we've hit something. Return the current i (distance)
            # if we did.
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= width or rotated_p[1] >= height:
                self._draw_water_track_sensor(rotated_p)
                return 700  # Sensor is off the screen. return max distance
            else:
                obs = get_point_from_rgb_list((rotated_p[0] - self.bgx), height - rotated_p[1], self.track_rgb)
                if self.get_water_or_not(obs) != 0:
                    self._draw_water_track_sensor(rotated_p)
                    return i

        self._draw_water_track_sensor(rotated_p)
        return i

    @staticmethod
    def make_sonar_arm(x: float, y: float) -> list:
        """
        :return: list of points
        """
        spread = 1  # Default spread.
        arm_distance = 5 # Gap before first sensor.
        arm_points = []
        # Make an arm. We build it flat because we'll rotate it about the
        # center later.
        for i in range(1, 701):
            arm_points.append((arm_distance + x + (spread * i), y))

        return arm_points

    @staticmethod
    def make_water_arm(x: float, y: float) -> list:
        """
        :return: list of points
        """
        spread = 1  # Default spread.
        arm_distance = 5 # Gap before first sensor.
        arm_points = []
        # Make an arm. We build it flat because we'll rotate it about the
        # center later.
        for i in range(1, 701):
            arm_points.append((arm_distance + x + (spread * i), y))

        return arm_points

    @staticmethod
    def make_octopus_arm(x: float, y: float) -> list:
        """
        :return: list of points
        """
        spread = 1  # Default spread.
        arm_distance = 5 # Gap before first sensor.
        arm_points = []
        # Make an arm. We build it flat because we'll rotate it about the
        # center later.
        for i in range(1, 201):
            arm_points.append((arm_distance + x + (spread * i), y))

        return arm_points

    @staticmethod
    def get_rotated_point(x_1: float, y_1: float, x_2: float, y_2: float, radians: float) -> (float, float):
        """
        Computes rotated points for sonar arms

        :param x_1: sub x
        :param y_1: sub y
        :param x_2: sonar arm x
        :param y_2: sonar arm y
        :param radians: sonar arm angle

        :return: Point for sonar arm
        """
        # Rotate x_2, y_2 around x_1, y_1 by angle.
        x_change = (x_2 - x_1) * math.cos(radians) + \
                   (y_2 - y_1) * math.sin(radians)
        y_change = (y_1 - y_2) * math.cos(radians) - \
                   (x_1 - x_2) * math.sin(radians)
        new_x = x_change + x_1
        new_y = height - (y_change + y_1)
        return int(new_x), int(new_y)

    def get_track_or_not(self, reading: list) -> int:
        """
        Checks if sub is in cave

        :param reading: A list representing a color

        :return: 0 or 1 indicating true or false
        """
        if reading == self.off_track_color:
            return 1
        else:
            return 0

    def get_water_or_not(self, reading: list) -> int:
        """
        Checks if sub is in the water

        :param reading: A list representing a color

        :return: 0 or 1 indicating true or false
        """
        if reading == self.water_color:
            return 1
        else:
            return 0

    def get_octopus_or_not(self, reading: list) -> int:
        """ 
        Checks if sub is getting hugged by an octopus

        :param reading: A list representing a color

        :return: 0 or 1
        """
        if reading == self.octopus_color:
            return 1
        else:
            return 0

    @property
    def ontrack(self) -> bool:
        return self.on_track

    @property
    def oxigenio(self) -> int:
        return self.oxygen

    @property
    def score(self) -> int:
        """
        :return: sub's score
        """
        return -1 * self.bgx * 10 + self.oxygen


class Simulation:
    def __init__(self, track, player2 = False):
        """
        Handles simulation and GUI
        :param track: Track object witch configures the scenario
        :param sub2: used for competition
        """

        # Initialize GUI if requested
        if evaluate:
            pygame.init()
            self.screen = pygame.display.set_mode((width, height))
            self.clock = pygame.time.Clock()
            self.screen.set_alpha(None)
            pygame.font.init()
            myfont = pygame.font.SysFont('Arial', 12)

        # Initialize class variables
        self.track = track
        self.frame_count = 0
        self.on_track = True
	#background
        self.global_track = Background(self.track.display_img_path, [0, 0])
	#
        self.max_steps = 1058
        self.game_objects = []

        # Physics stuff.
        self.space = pymunk.Space()
        self.space.gravity = pymunk.Vec2d(0., -100.)

        if player2 == True:
            self.player2 = True
        else:
            self.player2 = False

        # Record steps.
        self.num_steps = 0

        # More GUI stuff
        if evaluate:
            self.screen.fill(THECOLORS["black"])
            self.global_track.render(self.screen)
            pygame.display.flip()
            self.textsurface = myfont.render('Oxigenio: ', False, (255, 255, 255))
        self.global_track.update()

        # Track variables
        self.image = Image.open(self.track.mask_img_path)
        self.image = self.image.resize((bwidth, 700))
        self.track_rgb = list(self.image.getdata())
        self.off_track_color = (128,127,0,255)
        self.water_color = (0, 0, 255, 255)
        self.octopus_color = (255, 0, 0, 255)

        # GUI stuff
        if evaluate:
            game_screen = self.screen
        else:
            game_screen = None

        # Creates player sub
        self.sub1 = _Sub(self.space, self.track, self.track.sub1_position, self.track.initial_oxygen, self.track_rgb, self.off_track_color,
                         sub_image, self.global_track, self.water_color, self.octopus_color, screen=game_screen)

        if self.player2 == True:
            self.sub2 = _Sub(self.space, self.track, self.track.sub2_position, self.track.initial_oxygen, self.track_rgb, self.off_track_color,
                         sub2_image, self.global_track, self.water_color, self.octopus_color, screen=game_screen)

        self.game_objects.append(self.sub1)

        if self.player2 == True:
            self.game_objects.append(self.sub2)

    def reset(self):
        """
        Resets simulation
        """
        self.sub1.reset()
        self.global_track.reset()

        if self.player2 == True:
            self.sub2.reset()

    def frame_step(self, action: int) -> list:
        """
        Advances simulation by one frame.
        :param action: Action to be given to player's sub
        :return: sensors player's sub acquired by advancing frame.
        """
        self.frame_count += 1

        self.sub1.sub_step(action)

        if self.player2 == True:
            self.sub2.sub_step(action)


        self.space.step(1. / 10)
        self.global_track.update()

        if evaluate:
            block_print()
            self._draw_screen()
            enable_print()
        sensors = self.sub1.sensors

        if self.player2 == True:
            self.sub2.sensors

        return sensors

    def comp_frame_step(self):

        self.space.step(1. / 10)
        self.global_track.update()
        if evaluate:
            block_print()
            self._draw_screen()
            enable_print()
        pass

    def _draw_screen(self):
        self.global_track.render(self.screen)
        self.sub1.draw()
        if self.player2 == True:
            self.sub2.draw()

        draw(self.screen, self.space)

        #imprime oxigenio
        self.screen.blit(self.textsurface, (10, 682))

        self.clock.tick()

        pass
