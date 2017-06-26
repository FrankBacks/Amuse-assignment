import matplotlib.pyplot as plt

from amuse.units import units
from amuse.units import constants
from amuse.units import nbody_system

from initial_conditions import *
from make_animation import *

from amuse.community.hermite0.interface import Hermite
from amuse.community.huayno.interface import Huayno

from time import time as clock_time


# No separate evolve file (for now)
# from evolve.py import *

def main_function(number_of_stars=1000, end_time=10.0 | nbody_system.time,
                  steps=1000, number_of_workers=5, animate=True, save_animation=True,
                  Q=0.5, D=2.6, filename="default.mp4", use_huayno=False):
    """
    Simulates a cluster of stars with varying masses. 
    Input: 
    :param number_of_stars: Number of stars to simulate, default: 1000
    :param end_time:        Total time at which to stop in nbody_system.time units (I think), 
                            default 10 | nbody_system.time
    :param steps:           Total number of steps to save, default: 1000
    :param number_of_workers: Number of cores/threads to use, does nothing when using Huayno, default: 5
    :param animate:         Makes an animation of the stars at each step (size depends on star mass), default: True
    :param save_animation:  Saves the animation as mp4 file, default: True
    :param Q:               Kinectic to potential energy fraction (I think) default: 0.5
    :param D:               Measure of fragmentedness, must be between 1.5 and 3, default 2.6
    :param filename:        Determines the name of the mp4 file, default: "default.mp4"
    :param use_huayno:      Use alternative Huayno gravity evolver, default: False
    :return: (array of position arrays at each time step, array of time at each time step) 
    """

    start_time = clock_time()

    particles = new_cluster(number_of_stars=number_of_stars, Q=Q, D=D)
    particles.scale_to_standard()

    # Initialize gravity
    if use_huayno:
        gravity = Huayno(number_of_stars=number_of_stars)
    else:
        gravity = Hermite(number_of_workers=number_of_workers)

    gravity.parameters.epsilon_squared = 0.05 | nbody_system.length ** 2
    # gravity.parameters.epsilon_squared = 0.15 | nbody_system.length ** 2 # Used to be this
    gravity.particles.add_particles(particles)
    from_gravity_to_model = gravity.particles.new_channel_to(particles)

    # Initial time (note * end_time for correct units)
    time = 0.0 * end_time

    # Save initial conditions and make arrays (lists) for each step
    total_energy_at_t0 = gravity.kinetic_energy + gravity.potential_energy
    save_positions = [particles.position]
    save_masses = [particles.mass]
    times = [time]

    while time <= end_time:
        time += end_time / steps

        gravity.evolve_model(time)
        from_gravity_to_model.copy()

        # Save data
        save_positions.append(particles.position)
        save_masses.append(particles.mass)
        times.append(time)

        total_energy = gravity.kinetic_energy + gravity.potential_energy
        if np.abs((total_energy - total_energy_at_t0) / total_energy_at_t0) > 0.001:
            print("Warning! Total energy of the system is changing too significantly!")

        print "Time: %.4g" % time.number

    gravity.stop()

    print "It took %.3g seconds clock time" % (clock_time() - start_time)

    if animate:
        make_animation(save_positions, save_masses, times, save_animation=save_animation, filename=filename)

    return save_positions, times

# callable form command line (only with default settings)
# to run with different settings import it into a python environment (from main import *)
if __name__ == "__main__":
    main_function()


