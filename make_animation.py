# Import the whole lot for now, some are not required, but maybe later they will be required.

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from amuse.units import units
from amuse.units import constants
from amuse.units import nbody_system
from mpl_toolkits.mplot3d import Axes3D


def update_animation(i, graph, save_positions):
    graph._offsets3d = (save_positions[i][:, 0].number, save_positions[i][:, 1].number, save_positions[0][:, 2].number)
    return graph


def make_animation(save_positions, save_masses, times, save_animation=False, filename="default.mp4"):
    """
    Makes an animation! Yay! Returns nothing. For more information see main.py. 
    """
    f = plt.figure()
    ax = plt.subplot(111, projection="3d")
    graph = ax.scatter(save_positions[0][:, 0].number, save_positions[0][:, 1].number, save_positions[0][:, 2].number,
                       color="red", s=np.array(save_masses[0].number) * 1000)
    ax.set_xlim([-2.5, 2.5])
    ax.set_ylim([-2.5, 2.5])
    ax.set_zlim([-2.5, 2.5])

    ani = animation.FuncAnimation(f, update_animation, frames=len(times), fargs=(graph, save_positions), interval=20)

    if save_animation:
        ani.save(filename, writer="ffmpeg", bitrate=-1, codec="h264")

    plt.show()

