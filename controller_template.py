import simulator as simulator


class Controller:
    def __init__(self, track: 'Track', evaluate: bool = True):
        """
            This class creates a new racing simulation and implements the controller of a car.
            :param track: The racing track object to be used in the simulation
            :param evaluate: Sets if GUI is visible or not
        """
        simulator.evaluate = evaluate
        self.track = track
        self.sensors = []
        self.episode = 1
        self.track_name = track
        self.episode_length = track.episode_length
        self.game_state = simulator.Simulation(track)
        self.best_score = -float('inf')
        self.best_features = []
        pass

    def run_episode(self, parameters: list) -> int:

        self.episode += 1
        self.game_state.reset()
        self.sensors = self.game_state.frame_step(0)
        frame_current = 0
        episode_length = self.episode_length

        while frame_current <= 1058 and self.game_state.sub1.ontrack == True and self.game_state.sub1.oxigenio > 0:
                self.sensors = self.game_state.frame_step(self.take_action(parameters))
                #print(self.sensors)
                #print(self.compute_features(self.sensors))
                #print(self.action)
                frame_current += 1

        score = self.game_state.sub1.score

        return score

    def take_action(self, parameters: list) -> int:
        raise NotImplementedError("This Method Must Be Implemented")

    def compute_features(self, sensors: list) -> list:
        raise NotImplementedError("This Method Must Be Implemented")

    def learn(self, weights):
        raise NotImplementedError("This Method Must Be Implemented")
