#!/usr/bin/env python2
# -*- coding: utf-8 -*-\

import random
import argparse
import re
from timeit import default_timer as Timer


class User(object):

    def __init__(self):
        self.name = raw_input('\nEnter a player name: ').strip()
        self.player_score = 0

    def add_points(self, points):
        self.player_score += points


class ComputerPlayer(User):

    def __init__(self):
        self.name = raw_input('\nEnter the computer name: ').strip()

    def ai_strategy(self, pending_points):
        if pending_points >= 25 or pending_points >= (100 - self.player_score):
            return 'hold'
        else:
            return 'roll'


class PlayerFactory(object):
    def player_create(self, player_type):
        if player_type == 'CPU':
            return ComputerPlayer()
        elif player_type == 'HUMAN':
            return User()


class Dye(object):

    # Choose how many sides your dye has
    def __init__(self, sides):
        self.sides = [i + 1 for i in range(sides)]

    def roll(self):
        return random.choice(self.sides)


class PigGameInstance(object):

    def __init__(self):
        self.player_data = {}
        self.pending_points = 0
        self.current_player_turn = None

    def add_player(self, player):
        self.player_data[player.name] = player.player_score

    def check_if_winner(self):
        for key, val in self.player_data.items():
            if val >= 100:
                print '{} has won the game! \nWould you like to play again?\n'.format(
                    key)
                self.reset_state()
                quit()

    def display_scores(self):
        # Format the dictionary entries and join the list to the string
        print '''\n################# SCOREBOARD #################\n\n{}\n\n##############################################\n
        '''.format(' \n'.join('{} : {}'.format(key, val) for (key, val) in self.player_data.items()))

    def reset_state(self):
        self.player_data.clear()
        self.pending_points = 0

    def get_current_player(self):
        return self.current_player_turn

    def player_turn(self):
        # Get input and validate
        while True:
            player_response = raw_input(
                'Will you Roll or Hold? (r,h and roll,hold are valid answers)\n').strip()
            if not re.match(r'(roll|hold|r|h)', player_response, flags=re.IGNORECASE):
                print 'Please enter a valid move.'
                continue
            else:
                return player_response
                break


class TimedGameProxy(PigGameInstance):
    def __init__(self):
        self.game_length = 60.0
        self.game_timer = None


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument(
        '--player1', help='Set whether Player 1 is a human or computer.', required=True)
    parse.add_argument(
        '--player2', help='Set whether Player 2 is a human or computer.', required=True)
    parse.add_argument(
        '--timed', help='Play a timed version of Pig y/n', required=False, default=None)
    args = parse.parse_args()

    # Check then initialize proper game type
    if args.timed == 'y':
        pig_game = TimedGameProxy()
        # pig.game_timer()
        # Add players to the game
        factory = PlayerFactory()
        player1 = factory.player_create('CPU') if re.match(
            r'(cpu|computer)', args.player1, flags=re.IGNORECASE) else factory.player_create('HUMAN')
        player2 = factory.player_create('CPU') if re.match(
            r'(cpu|computer)', args.player2, flags=re.IGNORECASE) else factory.player_create('HUMAN')
    else:
        pig_game = PigGameInstance()
        player_count = int(
            raw_input('Set amount of players for this game: ').strip())
        for _ in range(player_count):
            pig_game.add_player(User())

    game_dye = Dye(6)

    print '\n***~\~\~\~\~\~\~####### WELCOME TO PIG! #######~/~/~/~/~/~/~***\n'
    print '''
            (\____/)
            / @__@ |
           (  (oo)  )
            `-.~~.-'
             /    |
           @/      \_
          (/ /    \ \)
           WW`----'WW 

           By David Ally\n'''.center(30)
    print '''
    Pig is a game of chance, but also of great skill!
    Prove your bravery by testing your luck, fortune may yet smile upon you.
    Or cower in fear and hold back on your meager earnings like the pathetic 
    weakling you are...

    Are you ready, great warriors of the keyboard?
    '''.center(6)

    while pig_game:

        for key, val in pig_game.player_data.items():
            pig_game.current_player_turn = key
            curr_player = pig_game.get_current_player()
            bad_roll = False

            # If the roll is bad then the next player will have their turn
            while bad_roll == False:
                print '\nIt\'s {}\'s turn: '.format(key)
                response = pig_game.player_turn()
                print '\n'
                if re.match(r'(roll|r)', response, flags=re.IGNORECASE):
                    current_roll = game_dye.roll()
                    if current_roll == 1:
                        print '{} rolled a 1: Ooh.. bad luck! \n'.format(key)
                        bad_roll = True
                        pig_game.pending_points = 0
                        break
                    else:
                        print '\n{} rolled a: {}'.format(key, current_roll)
                        pig_game.pending_points += current_roll
                        pig_game.display_scores()
                        print 'Pending points: {} \n'.format(
                            pig_game.pending_points)
                        pig_game.check_if_winner()
                else:
                    pig_game.player_data[curr_player] += pig_game.pending_points
                    pig_game.pending_points = 0
                    break


if __name__ == '__main__':
    main()
