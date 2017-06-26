import matplotlib.pyplot as plt

from amuse.units import units
from amuse.units import constants
from amuse.units import nbody_system

from initial_conditions import *
from make_animation import *

from amuse.community.hermite0.interface import Hermite


# No separate evolve file (for now)
# from evolve.py import *

def main_function(number_of_stars=1000, end_time=10.0 | nbody_system.time,
                  steps=1000, number_of_workers=5, animate=True, save_animation=True):
    particles = new_cluster(number_of_stars=number_of_stars)
    particles.scale_to_standard()

    # Initialize gravity
    gravity = Hermite(number_of_workers=number_of_workers)
    gravity.parameters.epsilon_squared = 0.05 | nbody_system.length ** 2
    # gravity.parameters.epsilon_squared = 0.15 | nbody_system.length ** 2 # Used to be this
    gravity.particles.add_particles(particles)
    from_gravity_to_model = gravity.particles.new_channel_to(particles)

    time = 0.0 * end_time

    # Save initial conditions
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

    if animate:
        make_animation(save_positions, save_masses, times, save_animation=save_animation)

    return save_particles, times

main_function()


