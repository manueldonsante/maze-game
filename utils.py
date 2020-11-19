import numpy as np
import matplotlib.pyplot as plt


def show_env(env, fname=None):

    nrow, ncol = env.maze.shape
    
    ax = plt.gca()
    
    # Major ticks
    ax.set_xticks(np.arange(0, ncol, 1))
    ax.set_yticks(np.arange(0, nrow, 1))
    # Labels for major ticks
    ax.set_xticklabels(np.arange(1, ncol+1, 1))
    ax.set_yticklabels(np.arange(1, nrow+1, 1))
    # Minor ticks
    ax.set_xticks(np.arange(1, ncol+1, 1), minor=True)
    ax.set_yticks(np.arange(1, ncol+1, 1), minor=True)

    
    # Gridlines based on minor ticks
    ax.grid(which='minor', color='w', linestyle='-', linewidth=2)
    
    canvas = np.copy(env.maze)
    agent, mode = env.state
    canvas[agent] = 0.5   # agent cell
    for cell in env.visited:
        if env.visited[cell]:
            canvas[cell] = env.visited_mark
    img = plt.imshow(canvas, interpolation='none', cmap='gray')
    #ax.grid(which='major', color='w', linestyle='-', linewidth=0.1)
    if fname:
        plt.savefig(fname)
    return img
