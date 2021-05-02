import os
from game import Game
from agent import Agent


class Manager:
    def __init__(self):
        self.agents = [Agent(epsilon=0.1),
                       Agent(epsilon=0.1)]

    def play_game(self):
        '''play a single game between agents'''
        game = Game()
        player = 0
        states = [[None], [None]]
        actions = [[None], [None]]

        t = 0
        while True:
            agent = self.agents[player]
            states[player].append(game.get_state(player))
            action = agent.move(states[player][-2],
                                actions[player][-1],
                                0,
                                states[player][-1])
            actions[player].append(action)
            game.move(action)

            if game.done:
                reward = 1 if player == game.winner else -1
                agent.move(states[player][-1],
                           actions[player][-1],
                           reward,
                           None)
                self.agents[1-player].move(states[1-player][-1],
                                           actions[1-player][-1],
                                           -reward,
                                           None)
                break
            print(f"{t:3} Player {player} moved {action} score {game.score}")
            if t%100 == 0:
                print(game)

            player = 1 - player
            t += 1

    def load_agents(self):
        '''load agents from file if they exist'''
        if os.path.exists('agent0') and os.path.exists('agent1'):
            self.agents[0].load('agent0')
            self.agents[1].load('agent1')
            return True
        return False

    def save_agents(self):
        '''save agent weights to file'''
        self.agents[0].save('agent0')
        self.agents[1].save('agent1')


if __name__ == '__main__':
    m = Manager()
    m.load_agents()

    m.save_agents()
    for i in range(1):
        print("\nPlaying game {I}")
        m.play_game()
    
    m.save_agents()