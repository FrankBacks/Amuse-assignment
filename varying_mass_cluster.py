"""
Evolves an equal mass stellar cluster.
"""
from __future__ import print_function

import numpy

from matplotlib import pyplot
from amuse.units import units
from amuse.units import constants
from amuse.units import nbody_system
from amuse.units.generic_unit_converter import ConvertBetweenGenericAndSiUnits
from amuse.community.hermite0.interface import Hermite
from amuse.ic.plummer import new_plummer_model
from amuse.ic.salpeter import new_salpeter_mass_distribution
from amuse.datamodel import ParticlesWithUnitsConverted
import logging

import matplotlib.animation as animation

from amuse.ic.plummer import new_plummer_model

#logging.basicConfig(level=logging.DEBUG)

smoothing_length = 0.0 | nbody_system.length ** 2


def print_log(time, gravity, particles, total_energy_at_t0):
    kinetic_energy = gravity.kinetic_energy
    potential_energy = gravity.potential_energy
    total_energy_at_this_time = kinetic_energy + potential_energy
    print("time                    : " , time)
    print("energy error            : " , (total_energy_at_this_time - total_energy_at_t0) / total_energy_at_t0)


def new_cluster(number_of_stars = 1000):
    masses = new_salpeter_mass_distribution(
        number_of_stars, 
        mass_min = 0.1 | units.MSun,
        mass_max = 125.0 | units.MSun, 
        alpha = -2.35
    )
    nbody_converter = nbody_system.nbody_to_si(masses.sum(), 1 | units.parsec)
    particles = new_plummer_model(number_of_stars, nbody_converter)
    particles.mass = masses
    particles.move_to_center()
    print(particles)
    # particles2 = ParticlesWithUnitsConverted(
    #     particles,
    #     nbody_converter.as_converter_from_si_to_nbody())
    # print(particles2)

    particles.scale_to_standard(convert_nbody=nbody_converter)
    print(particles)
    return particles


def simulate_small_cluster(
        number_of_stars = 1000, 
        end_time = 40 | nbody_system.time,
        number_of_workers = 1
    ):
    particles = new_cluster(number_of_stars)

    converter = ConvertBetweenGenericAndSiUnits(1 | units.MSun, constants.G, 1e6 | units.yr)

    # particles.scale_to_standard()
   
    gravity = Hermite(converter, number_of_workers = number_of_workers)
    gravity.parameters.epsilon_squared = 0.15 | nbody_system.length ** 2
    
    gravity.particles.add_particles(particles)
    
    from_gravity_to_model = gravity.particles.new_channel_to(particles)
    
    time = 0.0 * end_time
    total_energy_at_t0 = gravity.kinetic_energy + gravity.potential_energy
    
    positions_at_different_times = []
    positions_at_different_times.append(particles.position)
    times = []
    times.append(time)
    
    print("evolving the model until t = " + str(end_time))
    while time < end_time:
        time += end_time / 1000.0
        
        gravity.evolve_model(time)
        from_gravity_to_model.copy()
        
        positions_at_different_times.append(particles.position)
        times.append(time)
        print_log(time, gravity, particles, total_energy_at_t0)
        
    gravity.stop()
    
    return times, positions_at_different_times, particles.mass


def adjust_spines(ax,spines, ticks):
    for loc, spine in ax.spines.iteritems():
        if loc in spines:
            spine.set_position(('outward',10)) # outward by 10 points
            spine.set_smart_bounds(True)
        else:
            spine.set_color('none') # don't draw spine

    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
        ax.yaxis.set_ticks(ticks)
    else:
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
        ax.xaxis.set_ticks(ticks)

    else:
        ax.xaxis.set_ticks([])


def plot_positions(times, positions_at_different_times):
    figure = pyplot.figure()
    plot_matrix_size = numpy.ceil(numpy.sqrt(len(positions_at_different_times))).astype(int)
    number_of_rows = len(positions_at_different_times) / plot_matrix_size
    figure.subplots_adjust(wspace = 0.15, hspace = 0.15)
    
    for index, (time, positions) in enumerate(zip(times, positions_at_different_times)):
        subplot = figure.add_subplot(plot_matrix_size, plot_matrix_size, index + 1)
        
        subplot.scatter(
            positions[...,0].number,#.value_in(nbody_system.length),
            positions[...,1].number,#.value_in(nbody_system.length),
            s = 1,
            edgecolors = 'red',
            facecolors = 'red'
        )
        
        # subplot.set_xlim(-4.0,4.0)
        # subplot.set_ylim(-4.0,4.0)
        
        title = 'time = {0:.2f}'.format(time.value_in(nbody_system.time))
        
        subplot.set_title(title)#, fontsize=12)
        spines = []
        if index % plot_matrix_size == 0:
            spines.append('left')

        if index >= ((number_of_rows - 1)*plot_matrix_size):
            spines.append('bottom')
            

        adjust_spines(subplot, spines,numpy.arange(-4.0,4.1, 1.0))
        
        if index % plot_matrix_size == 0:
            subplot.set_ylabel('y')
            
        if index >= ((number_of_rows - 1)*plot_matrix_size):
            subplot.set_xlabel('x')
            
    pyplot.show()


def update(i, positions_at_different_times, ax, masses):
    # ax[0].set_xdata(positions[i][..., 0].number)
    # ax[0].set_ydata(positions[i][..., 1].number)
    # ax = pyplot.scatter(positions_at_different_time[i][..., 0].number, positions_at_different_time[i][:, 1].number,
    #                     color="red", s=numpy.array(masses.number) / 1.e29)
    # pyplot.xlim([-1e17, 1e17])
    # pyplot.ylim([-1e17, 1e17])
    ax.set_offsets(zip(positions_at_different_time[i][...,0].number, positions_at_different_time[i][...,1].number))
    return ax

if __name__ == "__main__":
    times, positions_at_different_time, masses = simulate_small_cluster(1000, 9.0 | nbody_system.time, number_of_workers=5)
    # positions_at_different_time = numpy.array(positions_at_different_time)
    print(masses)
    f = pyplot.figure()
    ax = pyplot.scatter(positions_at_different_time[0][...,0].number, positions_at_different_time[0][:,1].number, color="red", s=numpy.array(masses.number) / 1.e29)
    pyplot.xlim([-1e17, 1e17])
    pyplot.ylim([-1e17, 1e17])

    ani = animation.FuncAnimation(f, update, frames=1000, fargs=(positions_at_different_time, ax, masses), interval=20)

    ani.save("Test02.mp4", writer="ffmpeg", bitrate=-1)

    pyplot.show()


    # plot_positions(times, positions_at_different_time)
