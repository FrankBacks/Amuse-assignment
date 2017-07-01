import matplotlib.pyplot as plt

from amuse.units import units
from amuse.units import constants
from amuse.units import nbody_system

from initial_conditions import *
from make_animation import *
from escape_stars import *

from amuse.community.hermite0.interface import Hermite
from amuse.community.huayno.interface import Huayno
from amuse.community.bhtree.interface import BHTree

from time import time as clock_time

from amuse.community.sse.interface import SSE


# No separate evolve file (for now)
# from evolve.py import *

def main_function(number_of_stars=1000, end_time=4.0e4 | units.yr, steps=100, number_of_workers=6,
                  animate=True, save_animation=False, escape=False, Q=0.5, D=2.6,
                  filename="default.mp4", use_huayno=False, use_tree=False):
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
    total_mass = particles.mass.sum()
    convert_nbody = nbody_system.nbody_to_si(total_mass, 1.0 | units.parsec)

    # Initialize gravity can use others for tests, but hermite is used
    if use_huayno:
        gravity = Huayno(convert_nbody, number_of_workers=number_of_workers / 2)
    elif use_tree:
        gravity = BHTree(convert_nbody, number_of_workers=1, epsilon_squared=0.05 | nbody_system.length**2)
    else:
        gravity = Hermite(convert_nbody, number_of_workers=number_of_workers / 2)

    gravity.parameters.epsilon_squared = 0.05 | nbody_system.length ** 2
    # gravity.parameters.epsilon_squared = 0.15 | nbody_system.length ** 2 # Used to be this
    gravity.particles.add_particles(particles)
    from_gravity_to_model = gravity.particles.new_channel_to(particles)

    # particles.scale_to_standard() Cannot scale to standard if not using nbody_system units

    # Initialize the Evolution
    if not use_tree:
        stellar_evolution = SSE(number_of_workers=number_of_workers / 2)
    else:
        stellar_evolution = SSE(number_of_workers=number_of_workers - 1)
    stellar_evolution.particles.add_particles(particles)
    from_stellar_evolution_to_model = stellar_evolution.particles.new_channel_to(particles)
    from_stellar_evolution_to_model.copy_attributes(["mass", "luminosity", "temperature"])

    # Initial time (note * end_time for correct units)
    time = 0.0 * end_time

    # Save initial conditions and make arrays (lists) for each step
    total_energy_at_t0 = gravity.kinetic_energy + gravity.potential_energy
    save_positions = [particles.position]
    save_velocities = [particles.velocity]
    save_masses = [particles.mass]
    save_luminosities = [particles.luminosity]
    save_temperatures = [particles.temperature]
    times = [time]

    while time < end_time:
        time += end_time / steps

        # Evolve gravity
        gravity.evolve_model(time)
        from_gravity_to_model.copy()

        # Evolve stars
        stellar_evolution.evolve_model(time)
        from_gravity_to_model.copy()
        from_stellar_evolution_to_model.copy_attributes(["mass", "luminosity", "temperature"])

        # Save data
        save_positions.append(particles.position)
        save_velocities.append(particles.velocity)
        save_masses.append(particles.mass)
        save_luminosities.append(particles.luminosity)
        save_temperatures.append(particles.temperature)
        times.append(time)

        total_energy = gravity.kinetic_energy + gravity.potential_energy
        if np.abs((total_energy - total_energy_at_t0) / total_energy_at_t0) > 0.001:
            print("Warning! Total energy of the system is changing too significantly!")

        print "Time: %.4g" % time.number
        total_mass = particles.mass.sum()
        print total_mass

    if escape:
        escaped_stars_3d, escaped_stars_2d = find_escapees(particles)

    gravity.stop()
    stellar_evolution.stop()
    print "It took %.3g seconds clock time" % (clock_time() - start_time)

    if animate:
        make_animation(save_positions, save_luminosities, save_temperatures,
                       times, save_animation=save_animation, filename=filename)
    if escape:
        return save_positions[-1], save_velocities[-1], save_masses[-1], escaped_stars_3d, escaped_stars_2d
    else:
        return save_positions, save_velocities

# callable form command line (only with default settings)
# to run with different settings import it into a python environment (from main import *)
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--number_of_stars", default=1000)
    parser.add_argument("--number_of_workers", default=6)
    parser.add_argument("--steps", default=1000)
    parser.add_argument("--save_animation", default=False)
    parser.add_argument("--end_time", default=4.e6)  # in years, unit added later
    parser.add_argument("--filename", default="default.mp4")
    parser.add_argument("--use_tree", default=False)
    parser.add_argument("--use_huayno", default=False)
    parser.add_argument("--Q", default=0.5)
    parser.add_argument("--D", default=2.6)
    parser.add_argument("--escape", default=False)
    # parser.add_argument("", default=)
    args = parser.parse_args()

    kwarg_dict = {"number_of_stars": int(args.number_of_stars),
                  "number_of_workers": int(args.number_of_workers),
                  "steps": int(args.steps),
                  "save_animation": bool(args.save_animation),
                  "end_time": float(args.end_time) | units.yr,
                  "filename": str(args.filename),
                  "use_tree": bool(args.use_tree),
                  "use_huayno": bool(args.use_huayno),
                  "Q": float(args.Q),
                  "D": float(args.D),
                  "escape": bool(args.escape)}
    a = main_function(**kwarg_dict)


