import numpy
from amuse.units import units
from amuse.units import constants
from amuse.ic.brokenimf import new_broken_power_law_mass_distribution
from amuse.ic.fractalcluster import new_fractal_cluster_model


def new_cluster(D, Q, number_of_stars = 1000):
    masses = new_broken_power_law_mass_distribution(number_of_stars, mass_boundaries=[0.08, 0.1, 0.5, 50.0] | units.MSun, alphas=[-0.3, -1.3, -2.3])

    particles = new_fractal_cluster_model(masses = masses, do_scale=True, fractal_dimension = D, virial_ratio = Q)

    particles.move_to_center()

    return particles

new_cluster(D = 2.6, Q = 0.5, number_of_stars = 1000)
