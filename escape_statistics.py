"""
Runs the simulation multiple times with the same settings to find the properties of the escaping stars
"""

from main import *

def escape_properties():

    # D=2.6 Q=0.5 (hot)
    # D=1.6 Q=0.3 (cool)

    escape_velocities_hot = []
    escape_masses_hot = []
    number_of_escaped_stars_2d_hot = []
    number_of_escaped_stars_3d_hot = []

    escape_velocities_cool = []
    escape_masses_cool = []
    number_of_escaped_stars_2d_cool = []
    number_of_escaped_stars_3d_cool = []

    for i in range(10):
        positions, velocities, masses, escaped_stars_3d, escaped_stars_2d = \
            main_function(Q=0.5, D=2.6, animate=False, end_time=4.e7 | units.yr, number_of_stars=1000, steps=100, escape=True)

        # Only visible velocities for Gaia
        escape_velocities_hot += list(np.sum(velocities[escaped_stars_3d].number[:,:2]**2, axis=1)**0.5)
        escape_masses_hot += list(masses[escaped_stars_3d].number)

        number_of_escaped_stars_2d_hot += [np.sum(escaped_stars_2d)]
        number_of_escaped_stars_3d_hot += [np.sum(escaped_stars_3d)]

        positions, velocities, masses, escaped_stars_3d, escaped_stars_2d = \
            main_function(Q=0.3, D=1.6, animate=False, end_time=4.e7 | units.yr, number_of_stars=1000, steps=100, escape=True)

        escape_velocities_cool += list(np.sum(velocities[escaped_stars_3d].number**2, axis=1)**0.5)
        escape_masses_cool += list(masses[escaped_stars_3d].number)

        number_of_escaped_stars_2d_cool += [np.sum(escaped_stars_2d)]
        number_of_escaped_stars_3d_cool += [np.sum(escaped_stars_3d)]

    print escape_velocities_cool
    np.savetxt("escape_masses_hot", escape_masses_hot)
    np.savetxt("escape_velocities_hot", escape_velocities_hot)
    np.savetxt("number_of_escaped_stars_hot_2d_3d", [number_of_escaped_stars_3d_hot, number_of_escaped_stars_2d_hot])

    np.savetxt("escape_masses_cool", escape_masses_cool)
    np.savetxt("escape_velocities_cool", escape_velocities_cool)
    np.savetxt("number_of_escaped_stars_cool_2d_3d", [number_of_escaped_stars_3d_cool, number_of_escaped_stars_2d_cool])


if __name__ == "__main__":
    escape_properties()



