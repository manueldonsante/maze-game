import numpy as np
import Environment
import utils



maze =  np.array([
    [ 1.,  0.,  1.,  1.,  1.,  1.,  1.],
    [ 1.,  1.,  1.,  0.,  0.,  1.,  0.],
    [ 0.,  0.,  1.,  1.,  1.,  1.,  0.],
    [ 1.,  1.,  1.,  1.,  1.,  0.,  1.],
    [ 1.,  0.,  0.,  0.,  1.,  1.,  1.],
    [ 1.,  0.,  1.,  1.,  1.,  1.,  1.],
    [ 1.,  1.,  1.,  0.,  1.,  1.,  1.]
])



env = Environment.Maze(maze)

env.act(3)
env.act(2)
env.act(2)
env.act(1)
env.act(2)
utils.show_env(env)


'''
done = False

while not done:
    env_state, reward, status = env.act(1)
    print(env_state)
    utils.show_env(env)'''