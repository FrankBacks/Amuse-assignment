# Import the whole lot for now, some are not required, but maybe later they will be required.

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from amuse.units import units
from amuse.units import constants
from amuse.units import nbody_system
from mpl_toolkits.mplot3d import Axes3D


def make_colors(temperatures):
    """
    Makes an array of rgb colors ((r, g, b), ...)
    Temperatures should not have units
    """
    r = 1 - temperatures / 40000.
    r[r < 0] = 0

    g = temperatures / 40000.
    g[g > .5] = 1 - g[g > .5]
    g[g < 0] = 0
    g[g > 1] = 1

    b = temperatures / 40000.
    b[b > 1] = 1

    return zip(r**2, g**2, b**2)


def update_animation(i, graph, save_positions, save_luminosities, save_temperatures):
    graph._offsets3d = (save_positions[i][:, 0].number, save_positions[i][:, 1].number, save_positions[0][:, 2].number)
    # graph._sizes3d = np.array(save_luminosities[i].in_(units.LSun).number) * 10
    graph._sizes3d = (np.log10(save_luminosities[i].in_(units.J / units.s).number) - 22.)**2
    graph._colors3d = make_colors(save_temperatures[i].number)
    return graph


def make_animation(save_positions, save_luminosities, save_temperatures,
                   times, save_animation=False, filename="default.mp4"):
    """
    Makes an animation! Yay! Returns nothing. For more information see main.py. 
    """
    f = plt.figure(figsize=(10, 10))
    ax = plt.subplot(111, projection="3d")
    sizes = (np.log10(save_luminosities[0].in_(units.J / units.s).number) - 23.)**2
    colors = make_colors(save_temperatures[0].number)

    graph = ax.scatter(save_positions[0][:, 0].number, save_positions[0][:, 1].number, save_positions[0][:, 2].number,
                       c=colors, s=sizes)

    lim = save_positions[0].number.max()
    ax.set_xlim([-lim * 2, lim * 2])
    ax.set_ylim([-lim * 2, lim * 2])
    ax.set_zlim([-lim * 2, lim * 2])

    ani = animation.FuncAnimation(f,
                                  update_animation,
                                  frames=len(times),
                                  fargs=(graph, save_positions, save_luminosities, save_temperatures),
                                  interval=20)

    if save_animation:
        ani.save(filename, writer="ffmpeg", bitrate=-1, codec="h264")

    plt.show()

