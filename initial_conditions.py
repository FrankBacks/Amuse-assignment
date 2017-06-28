import numpy
from amuse.units import units
from amuse.units import constants
from amuse.units import nbody_system
from amuse.ic.brokenimf import new_broken_power_law_mass_distribution
from amuse.ic.fractalcluster import new_fractal_cluster_model


def new_cluster(D=2.6, Q=0.5, number_of_stars = 10):
    masses = new_broken_power_law_mass_distribution(number_of_stars, mass_boundaries=[0.08, 0.1, 0.5, 50.0] | units.MSun, alphas=[-0.3, -1.3, -2.3])
    convert_nbody = nbody_system.nbody_to_si(masses.sum(), 1.0 | units.parsec)
    particles = new_fractal_cluster_model(convert_nbody=convert_nbody, masses = masses, fractal_dimension = D, virial_ratio = Q, do_scale=True)

    particles.move_to_center()

    return particles

if __name__ == "__main__":
    # Just a test case :)
    print new_cluster(D = 2.6, Q = 0.5, number_of_stars = 10)
