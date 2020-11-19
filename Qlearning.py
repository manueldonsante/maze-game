import numpy as np

class Qlearning:
    def __init__(self, env):
        self.learning_rate = 0.1
        self.discount = 0.95
        self.episodes = 25000
        self.show_every = 2000
        
        self.epsilon = 0.5
        self.start=eps=decay = 1
        self.end_eps_decay = self.episodes // 2
        
        erow, ecol = env.maze.shape
        q_table = np.zeros(erow*ecol, env.num_actions)
        
