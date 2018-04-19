"""
This module implements the Cave class, which defines all possible caves used in the game

Attributes:
    cave_list (list): Global variable that saves all possible Caves
"""

import os


cave_list = []


class Cave:
    def __init__(self, binary_img_path: str, display_img_path: str, name: str):
        """
        Class that defines a single cave
        
        :param binary_img_path: Location of the binary cave image
        :param display_img_path: Location of the image that will be displayed 
        :param name: Name of the cave used for identification/specification in the command line. 
        """
        self.mask_img_path = os.path.abspath(binary_img_path)
        if os.environ.get('OS','') == 'Windows_NT':
            self.display_img_path = display_img_path
        else:
            self.display_img_path = os.path.abspath(display_img_path)
        self.name = name
        self.episode_length = 1058

        self._sub1_position = None
        self._sub2_position = None
        self._angle_of_subs = None
        self._episode_length = None
        self._initial_oxygen = None

        cave_list.append(self)

    @property
    def sub1_position(self) -> (float, float):
        """
        :return: Position of first sub
        """
        if self._sub1_position is None:
            raise(ValueError("sub1_position not assigned"))
        return self._sub1_position

    @sub1_position.setter
    def sub1_position(self, value: (float, float)):
        self._sub1_position = value

    @property
    def sub2_position(self) -> (float, float):
        """
        :return: Position of second sub (this can be a bot or a second player)
        """
        if self._sub2_position is None:
            raise(ValueError("sub2_position not assigned"))
        return self._sub2_position

    @sub2_position.setter
    def sub2_position(self, value: (float, float)):
        self._sub2_position = value

    @property
    def angle_of_subs(self) -> float:
        """
        :return: Angle in radians
        """
        if self._angle_of_subs is None:
            raise(ValueError("angle_of_subs not assigned"))
        return self._angle_of_subs

    @angle_of_subs.setter
    def angle_of_subs(self, value: float):
        self._angle_of_subs = value

    @property
    def episode_length(self) -> int:
        """
        :return: Number of maximum frames an episode will be executed when using this cave
        """
        if self._angle_of_subs is None:
            raise(ValueError("episode_limit not assigned"))
        return self._episode_length

    @episode_length.setter
    def episode_length(self,value: int):
        self._episode_length = value

    @property
    def initial_oxygen(self):
        """
        :return: Initial amount of oxygen in the submarine
        """
        if self._initial_oxygen is None:
            raise(ValueError("initial oxygen not assigned"))
        return self._initial_oxygen

    @initial_oxygen.setter
    def initial_oxygen(self,value: int):
        self._initial_oxygen = value
