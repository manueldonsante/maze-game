import numpy as np
import matplotlib.pyplot as plt



class Maze:
    def __init__(self, maze, agent=(0,0)):
        """
        maze: a 2d Numpy array of 0's and 1's
            1.00 - a free cell
            0.50 - agent cell
            0.00 - an occupied cell (wall)
        agent: (row, col) initial agent position (defaults to (0,0)) """
        
        self.visited_mark = 0.8    # Cells visited by the agent will be painted by gray 0.8
        self.agent_mark = 0.5      # The current agent cell will be painteg by gray 0.5
        
        # Actions dictionary
        self.actions_dict = {
            'left': 0,
            'up': 1,
            'right' : 2,
            'down' : 3,
            }
        self.num_actions = len(self.actions_dict)
        
        self._maze = np.array(maze)
        nrows, ncols = self._maze.shape
        self.agent = agent   # agent position
        self.target = (nrows-1, ncols-1)   # target cell at bottom right
        self.free_cells = set((r,c) for r in range(nrows) for c in range(ncols) if self._maze[r,c] == 1.0)
        self.free_cells.discard(self.target)
        
        if self._maze[self.target] == 0.0:
            raise Exception("Invalid Maze: target cell in an occupied cell (wall)!")
        if not agent in self.free_cells:
            raise Exception("Invalid Agent Location: must sit on a free cell")
        
        self.reset(agent)
        
    def reset(self, agent=(0,0)):
        self.agent = agent
        self.maze = np.copy(self._maze)
        nrows, ncols = self.maze.shape
        row, col = agent
        self.maze[row, col] = self.agent_mark
        self.state = ((row, col), 'start')
        self.visited = dict(((r,c),0) for r in range(nrows) for c in range(ncols) if self._maze[r,c] == 1.0)
        self.total_reward = 0
        self.min_reward = -0.5 * self.maze.size
        self.base = np.sqrt(self.maze.size)
        self.reward = {
            'blocked':  self.min_reward,
            'invalid': -4.0/self.base,
            'valid':   -1.0/self.maze.size
        }
        
    def print_env_param(self):
        print(self.__dict__)
        
    
    def act(self, action):
        self.update_state(action)
        reward = self.get_reward()
        self.total_reward += reward
        status = self.game_status()
        env_state = self.observe()
        return env_state, reward, status

    def get_reward(self):
        agent, mode = self.state
        if agent == self.target:
            return 1.0
        if mode == 'blocked':
            return self.reward['blocked']
        elif mode == 'invalid':
            return self.reward['invalid']
        elif mode == 'valid':
            return self.reward['valid']
    
    
    def update_state(self, action):
        nrows, ncols = self.maze.shape
        (nrow, ncol), nmode = agent, mode = self.state
        
        if self.maze[agent] > 0.0:
            print(agent)
            self.visited[agent] += 1  # mark visited cell
            
        valid_actions = self.valid_actions()
                
        if not valid_actions:
            nmode = 'blocked'
        elif action in valid_actions:
            nmode = 'valid'   
            if action == 0:    # move left
                ncol -= 1
            elif action == 1:  # move up
                nrow -= 1
            if action == 2:    # move right
                ncol += 1
            elif action == 3:  # move down
                nrow += 1
        else:                  # invalid action, no change in rat position
            nmode = 'invalid'
        
        # new state
        agent = (nrow, ncol)
        self.state = (agent, nmode)
        
        
    def valid_actions(self, cell=None):
        if cell is None:
            (row, col), mode = self.state
        else:
            row, col = cell
        actions = [0, 1, 2, 3]         # 0=left, 1=up, 2=right, 3=down
        nrows, ncols = self.maze.shape
        if row == 0:
            actions.remove(1)
        elif row == nrows-1:
            actions.remove(3)

        if col == 0:
            actions.remove(0)
        elif col == ncols-1:
            actions.remove(2)

        if row>0 and self.maze[row-1,col] == 0.0:
            actions.remove(1)
        if row<nrows-1 and self.maze[row+1,col] == 0.0:
            actions.remove(3)

        if col>0 and self.maze[row,col-1] == 0.0:
            actions.remove(0)
        if col<ncols-1 and self.maze[row,col+1] == 0.0:
            actions.remove(2)
        
        return actions
    
    def game_status(self):
        if self.total_reward < self.min_reward:
            return 'lose'
        agent, mode = self.state
        if agent == self.target:
            return 'win'
        return 'ongoing'
    
    def observe(self):
        canvas = self.draw_env()
        env_state = canvas.reshape((1, -1))
        return env_state
    
    def draw_env(self):
        canvas = np.copy(self.maze)
        nrows, ncols = self.maze.shape
        # clear all visual marks
        for r in range(nrows):
            for c in range(ncols):
                if canvas[r,c] > 0.0:
                    canvas[r,c] = 1.0

        # draw the agent
        agent, mode = self.state
        canvas[agent] = self.agent_mark
        return canvas