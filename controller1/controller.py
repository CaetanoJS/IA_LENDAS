import controller_template as controller_template


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



    def learn(self, weights) -> list:
        """
        IMPLEMENT YOUR LEARNING METHOD (i.e. YOUR LOCAL SEARCH ALGORITHM) HERE

        HINT: you can call self.run_episode (see controller_template.py) to evaluate a given set of weights
        :param weights: initial weights of the controller (either loaded from a file or generated randomly)
        :return: the best weights found by your learning algorithm, after the learning process is over
        """
        raise NotImplementedError("This Method Must Be Implemented")
