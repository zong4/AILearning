# 狼人杀

import random
import time
now = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime())
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='./logic/log' + now + '.txt', level=logging.DEBUG)

from logic import Symbol, And, Or, Not, Implication, model_check

ROLES = ['citizen', 'werewolf', 'prophet']

class Game:
    def __init__(self):
        number = 5
        roles = {'citizen': 3, 'werewolf': 1, 'prophet': 1}

        players_name = ['player' + str(i) for i in range(number)]
        # self.symboles = [Symbol(player_name + ' is ' + role) for player_name in players_name for role in ROLES]
        knowledge_base = And(
            Or(Symbol('player0 is citizen'), Symbol('player0 is werewolf'), Symbol('player0 is prophet')),
            Not(And(Symbol('player0 is citizen'), Symbol('player0 is werewolf'))),
            Not(And(Symbol('player0 is citizen'), Symbol('player0 is prophet'))),
            Not(And(Symbol('player0 is werewolf'), Symbol('player0 is prophet'))),

            Or(Symbol('player1 is citizen'), Symbol('player1 is werewolf'), Symbol('player1 is prophet')),
            Not(And(Symbol('player1 is citizen'), Symbol('player1 is werewolf'))),
            Not(And(Symbol('player1 is citizen'), Symbol('player1 is prophet'))),
            Not(And(Symbol('player1 is werewolf'), Symbol('player1 is prophet'))),

            Or(Symbol('player2 is citizen'), Symbol('player2 is werewolf'), Symbol('player2 is prophet')),
            Not(And(Symbol('player2 is citizen'), Symbol('player2 is werewolf'))),
            Not(And(Symbol('player2 is citizen'), Symbol('player2 is prophet'))),
            Not(And(Symbol('player2 is werewolf'), Symbol('player2 is prophet'))),

            Or(Symbol('player3 is citizen'), Symbol('player3 is werewolf'), Symbol('player3 is prophet')),
            Not(And(Symbol('player3 is citizen'), Symbol('player3 is werewolf'))),
            Not(And(Symbol('player3 is citizen'), Symbol('player3 is prophet'))),
            Not(And(Symbol('player3 is werewolf'), Symbol('player3 is prophet'))),

            Or(Symbol('player4 is citizen'), Symbol('player4 is werewolf'), Symbol('player4 is prophet')),
            Not(And(Symbol('player4 is citizen'), Symbol('player4 is werewolf'))),
            Not(And(Symbol('player4 is citizen'), Symbol('player4 is prophet'))),
            Not(And(Symbol('player4 is werewolf'), Symbol('player4 is prophet'))),

            Or(Symbol('player0 is citizen'), Symbol('player1 is citizen'), Symbol('player2 is citizen'), Symbol('player3 is citizen'), Symbol('player4 is citizen')),
            Or(Symbol('player0 is werewolf'), Symbol('player1 is werewolf'), Symbol('player2 is werewolf'), Symbol('player3 is werewolf'), Symbol('player4 is werewolf')),
            Or(Symbol('player0 is prophet'), Symbol('player1 is prophet'), Symbol('player2 is prophet'), Symbol('player3 is prophet'), Symbol('player4 is prophet')),
        )


        # random roles
        self.players = []
        for player_name in players_name:
            role = random.choice(ROLES)
            roles[role] -= 1

            if roles[role] == 0:
                ROLES.remove(role)

            if role == 'citizen':
                player = Citizen(player_name, role)
            elif role == 'werewolf':
                player = Werewolf(player_name, role)
            elif role == 'prophet':
                player = Prophet(player_name, role)

            player.add_knowledge(knowledge_base, None, True)
            self.players.append(player)

    def run(self):
        day = 0
        while True:
            day += 1
            print('Day', day)

            dead = None
            for player in self.players:
                if player.get_role() == 'werewolf':
                    dead = player.kill(self.players)
            print(dead.get_name() + ' is dead')

            if len(self.players) == 2:
                print('Werewolf win')
                break

            symbol = Symbol(dead.get_name() + ' is ' + dead.get_role())
            for player in self.players:
                player.add_knowledge(symbol, None, True)
            print(symbol)
            print()

            prophet = None
            checked = None
            for player in self.players:
                player.say(self.players.index(player))
                if player.get_role() == 'prophet':
                    prophet = player
                    checked = player.check(self.players)
            print()

            symbol1 = Symbol(prophet.get_name() + ' is ' + prophet.get_role())
            symbol2 = Symbol(checked.get_name() + ' is ' + checked.get_role())
            for player in self.players:
                player.add_knowledge(symbol1, None, True)
                player.add_knowledge(symbol2, None, True)

            votes = []
            for player in self.players:
                votes.append(player.vote(self.players))
            print()

            target = max(set(votes), key = votes.count)
            self.players.remove(target)
            print(target.get_name() + ' is voted')
            print()

            if target.get_role() == 'werewolf':
                print('Citizen win')
                break

class Player:
    def __init__(self, name, role):
        self.name = name
        self.role = role

        self.knowledge = And(
            Symbol(self.name + ' is ' + self.role),
        )

    def get_name(self):
        return self.name
    
    def get_role(self):
        return self.role

    def add_knowledge(self, symbol1, symbol2, sure):
        if sure:
            self.knowledge = And(self.knowledge, symbol1)

        if symbol2:
            self.knowledge = And(self.knowledge, Implication(symbol1, symbol2))

    def get_knowledge(self):
        return self.knowledge
    
    def get_probabilities(self, players, target):
        probabilities = []
        for player in players:
            symbol = Symbol(player.get_name() + ' is ' + target)
            model_check(self.knowledge, symbol)
            probabilities.append((player, symbol.true / (symbol.true + symbol.false)))

        logger.info(self.knowledge)
        logger.info(probabilities)

        probabilities.sort(key = lambda x: x[1])
        return (probabilities[0], probabilities[-1])
    
class Citizen(Player):
    def say(self, id):
        print(self.get_name() + ' is ' + self.get_role())
        return 'citizen'
    
    def vote(self, players):
        target_min, target_max = self.get_probabilities(players, 'werewolf')
        if target_min[1] == target_max[1]:
            print(self.get_name() + ' give up voting')
            return None
        else:
            print(self.get_name() + ' voted ' + target_max[0].get_name())
            return target_max[0]

class Werewolf(Player):
    def say(self, id):
        print(self.get_name() + ' is citizen(lying)')
        return 'citizen'
    
    def vote(self, players):
        target_min, target_max = self.get_probabilities(players, 'prophet')
        if target_min[1] == target_max[1]:
            print(self.get_name() + ' give up voting')
            return None
        else:
            print(self.get_name() + ' voted ' + target_max[0].get_name())
            return target_max[0]

    
    def kill(self, players):
        target_min, target_max = self.get_probabilities(players, 'prophet')
        players.remove(target_max[0])
        return target_max[0]
    
class Prophet(Player):
    def say(self, id):
        print(self.get_name() + ' is ' + self.get_role())
        return 'prophet'
    
    def vote(self, players):
        target_min, target_max = self.get_probabilities(players, 'werewolf')
        if target_min[1] == target_max[1]:
            print(self.get_name() + ' give up voting')
            return None
        else:
            print(self.get_name() + ' voted ' + target_max[0].get_name())
            return target_max[0]
    
    def check(self, players):
        target_min, target_max = self.get_probabilities(players, 'werewolf')
        print(self.get_name() + ' checked ' + target_max[0].get_name() + ' is ' + target_max[0].get_role())
        return target_max[0]
    
Game().run()