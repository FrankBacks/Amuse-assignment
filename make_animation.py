import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from amuse.units import units
from amuse.units import constants
from amuse.units import nbody_system


def update_animation(i, ax, save_positions):
    ax.set_offsets(zip(save_positions[i][:,0].number, save_positions[i][:,1].number))
    # print save_particles[i].position[:,0].number
    return ax


def make_animation(save_positions, save_masses, times, save_animation=False):
    """
    Makes an animation!
    """
    f = plt.figure()
    ax = plt.scatter(save_positions[0][:,0].number, save_positions[0][:,1].number,
                     color="red", s=np.array(save_masses[0].number) * 1000)
    plt.xlim([-5, 5])
    plt.ylim([-5, 5])

    ani = animation.FuncAnimation(f, update_animation, frames=len(times), fargs=(ax, save_positions), interval=20)

    if save_animation:
        ani.save("Fractal_clusters.mp4", writer="ffmpeg", bitrate=-1, codec="h264")
        
    plt.show()

