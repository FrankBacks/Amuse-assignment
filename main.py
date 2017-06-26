import matplotlib.pyplot as plt

from amuse.units import units
from amuse.units import constants
from amuse.units import nbody_system

from initial_conditions.py import *
from make_animation.py import *

from amuse.community.hermite0.interface import Hermite

# No separate evolve file (for now)
# from evolve.py import *

def main_function(end_time=10.0 | nbody_system.time, steps=1000, number_of_workers=5, animate=False):

    particles = new_cluster()
    particles.scale_to_standard()
	
	# Things to save
	save_particles = []
	times = []

	# Initialize gravity
	gravity = Hermite(number_of_workers=number_of_workers)
	gravity.parameters.epsilon_squared = 0.15 | nbody_system.length ** 2
	gravity.particles.add_particles(particles)
	from_gravity_to_model = gravity.particles.new_channel_to(particles)

	time = 0.0 * end_time
	
	# Save initial conditions
	total_energy_at_t0 = gravity.kinetic_energy + gravity.potential_energy
	save_particles.append(particles)
	times.append(time)
	
	while time < end_time:
		time += end_time / steps
		
		
        gravity.evolve_model(time)
        from_gravity_to_model.copy()
        
		# Save data
        save_particles.append(particles.position)
        times.append(time)

		total_energy = gravity.kinetic_energy + gravity.potential_energy
		if np.abs((total_energy - total_energy_at_t0) / total_energy_at_t0) > 0.001:
			print("Warning! Total energy of the system is changing too significantly!")



	if animate:
		make_animation()

	return save_particles, times

		


