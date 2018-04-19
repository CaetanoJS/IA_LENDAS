"""
This module collects command line arguments and prepares everything needed to run the simulator/game

Example:
    To quickly start the game and observe sensor readings:

        $ python AISub.py -c cave1 play
"""
import os
import argparse
import random
import datetime
import time
import numpy
import pygame
import simulator
from controller1.controller import Controller
from controller2.controller import Controller as Controller2
import caves_config as cave

def play(cave_name: str) -> None:
    """
    Launches the simulator in a mode where the player can control each action with the arrow keys.

    :param str cave_name: Name of a cave, as defined in caves_config.py
    :param str b_type: String
    :rtype: None
    """
    play_controller = Controller(cave_name)
    game_state = play_controller.game_state
    play_controller.sensors = [53, 66, 100, 1, 172.1353274581511, 150, -1, 0, 0]
    frame_current = 0
    while frame_current <= 1100 and game_state.sub1.ontrack == True and game_state.sub1.oxigenio > 0:
        events = pygame.event.get()
        if len(events) > 0:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction = 1
                        feedback = game_state.frame_step(direction)
                        print("sensors  " + str(feedback))
                        print("features " + str(play_controller.compute_features(feedback)))
                        print("score    " + str(play_controller.game_state.sub1.score))

                    if event.key == pygame.K_q:
                        exit()
                    if event.key == pygame.K_r:
                        game_state.reset()
        else:
            direction = 2
            feedback = game_state.frame_step(direction)
            print("sensors  " + str(feedback))
            print("features " + str(play_controller.compute_features(feedback)))
            print("score    " + str(play_controller.game_state.sub1.score))
        frame_current += 1
        print(frame_current)

    pass


def parser() -> (argparse.Namespace, list):
    """
    Parses command line arguments.

    :return: a tuple containing parsed arguments and leftovers
    """
    p = argparse.ArgumentParser(prog='AISub.py')
    mode_p = p.add_subparsers(dest='mode')
    mode_p.required = True
    p.add_argument('-w', nargs=1,
                   help='Specifies the weights\' file path; if not specified, a random vector of weights will be '
                        'generated.\n')
    p.add_argument('-c', nargs=1,
                   help='Specifies the cave you want to select; by default, cave1 will be used. '
                        'Check the \'cave.py\' file to see the available caves/create new ones.\n')
    mode_p.add_parser('learn',
                      help='Starts %(prog)s in learning mode. This mode does not render the game to your screen, '
                           'resulting in '
                           'faster learning.\n')
    mode_p.add_parser('evaluate',
                      help='Starts %(prog)s in evaluation mode. This mode runs your AI with the weights/parameters '
                           'passed as parameter \n')
    mode_p.add_parser('play',
                      help='Starts %(prog)s in playing mode. You can control each action of the sub using the arrow '
                           'keys of your keyboard.\n')
    mode_p.add_parser('comp',
                      help="Starts %(prog)s in competition mode. Place the controller (controller.py) of player one in controller1/ "
                           "and the other player's controller in controller2/. The weights will be loaded from a file called \"weights.txt\" in "
                           "the same folder.\n")

    arguments, leftovers = p.parse_known_args()
    p.parse_args()
    return arguments, leftovers


def comp(a_track: 'Cave',weights_1: numpy.ndarray, weights_2: numpy.ndarray, sub1_points: int, sub2_points: int) -> (int, int):
    """
    Run competition safely

    :param weights_1: weights from controller 1
    :param weights_2: weights from controller 2
    :param sub1_points: controller1's score
    :param sub2_points: controller2's score

    :return: None
    """
    ctrl1 = Controller(chosen_cave, evaluate=False)
    ctrl2 = Controller2(chosen_cave, evaluate=False)

    simulator.evaluate = True
    simulation = simulator.Simulation(a_cave, player2 = True)
    simulation.frame_step(2)
    frame_current = 0
    episode_length = 1058

    while frame_current <= 1058 and simulation.sub1.ontrack == True and simulation.sub1.oxigenio > 0 and simulation.sub2.ontrack == True and simulation.sub2.oxigenio > 0:
        ctrl1.sensors = simulation.sub1.sensors
        ctrl2.sensors = simulation.sub2.sensors

        simulation.sub1.sub_step(ctrl1.take_action(weights_1))
        simulation.sub2.sub_step(ctrl2.take_action(weights_2))
        simulation.comp_frame_step()

        frame_current += 1

    if simulation.sub1.ontrack == False and simulation.sub2.ontrack == False:
        print("Empate. Player 1 e Player 2 -> Recebem 1 ponto")
        sub2_points += 1
        sub1_points += 1
    elif simulation.sub1.oxigenio <= 0 and simulation.sub2.oxigenio <= 0:
        print("Empate. Player 1 e Player 2 -> Recebem 1 ponto")
        sub2_points += 1
        sub1_points += 1       
    elif simulation.sub1.ontrack == False or simulation.sub1.oxigenio <= 0:
        print("Ganhador: Player 2 -> Recebe 3 pontos")
        sub2_points += 3
    elif simulation.sub2.ontrack == False or simulation.sub2.oxigenio <= 0:
        print("Ganhador: Player 1 -> Recebe 3 Pontos")
        sub2_points += 3

    return sub1_points, sub2_points


if __name__ == '__main__':

    args, trash = parser()

    # Selects cave; by default cave1 will be selected
    chosen_cave = cave.cave1
    if args.c is None:
        chosen_cave = cave.cave1
    else:
        for a_cave in cave.cave.cave_list:
            if args.c[0] == a_cave.name:
                chosen_cave = a_cave

    # Sets weights
    if args.w is None:
        ctrl_temp = Controller(chosen_cave, evaluate=False)
        fake_sensors = [700, 700, 700, 700, 700, 700, 700, 200, 200, 200, 200, 200, 400]
        features_len = len(ctrl_temp.compute_features(fake_sensors))
        weights = [random.uniform(-1, 1) for i in range(0, features_len * 2)]
    else:
        weights = numpy.loadtxt(args.w[0])


    # Starts simulator in play mode
    if str(args.mode) == 'play':
        play(chosen_cave)
    elif str(args.mode) == 'play2':
        play2(chosen_cave)
    # Starts simulator in evaluate mode
    elif str(args.mode) == 'evaluate':
        ctrl = Controller(chosen_cave)
        score = ctrl.run_episode(weights)
        print("Score: %d\n" % score)
    # Starts simulator in learn mode and saves the best results in a file
    elif str(args.mode) == 'learn':
        ctrl = Controller(chosen_cave, evaluate=False)
        result = ctrl.learn(weights)
        if not os.path.exists("./params"):
            os.makedirs("./params")
        output = "./params/%s.txt" % datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
        print(output)
        numpy.savetxt(output, result)

    elif str(args.mode) == 'comp':
        w_ctrl1 = numpy.loadtxt('controller1/weights.txt')
        w_ctrl2 = numpy.loadtxt('controller2/weights.txt')

        sub1_pts = 0
        sub2_pts = 0

        for a_cave in cave.cave.cave_list:
            print("Starting game in cave %s\n" % a_cave.name)
            sub1_pts, sub2_pts = comp(a_cave,w_ctrl1, w_ctrl2, sub1_pts, sub2_pts)
            print("Switching Starting Positions...\n")
            a_cave.sub1_position, a_cave.sub2_position = a_cave.sub2_position, a_cave.sub1_position
            sub1_pts, sub2_pts = comp(a_cave,w_ctrl1, w_ctrl2, sub1_pts, sub2_pts)
            a_cave.sub1_position, a_cave.sub2_position = a_cave.sub2_position, a_cave.sub1_position

        print("Total score player 1: %dpts" % sub1_pts)
        print("Total score player 2: %dpts" % sub2_pts)

        if sub1_pts > sub2_pts:
            print("Player 1 is the winner!!!")
        elif sub1_pts == sub2_pts:
            print("Oh no! It's a tie.")
        else:
            print("Player 2 is the winner!!!")
