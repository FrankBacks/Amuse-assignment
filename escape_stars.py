"""
Checks which stars escape based on the following criteria:
- Kinetic energy + potential energy > 0.
- Stars are at 2 * half mass radius from center of the cluster.
- Velocity of the star in radial direction is larger than tangent direction.
This all assumes that the stars a reasonably well behaved, 
so the center of mass is at (0, 0, 0)and there are no clumps flying off. 
"""
import numpy as np
import matplotlib.pyplot as plt
from amuse.units import constants


def find_escapees(particles):

    # # condition 1
    # potential_energy = particles.potential() * particles.mass
    # kinetic_energy_3d = np.sum(particles.velocity**2, axis=1) * 0.5 * particles.mass
    # kinetic_energy_2d = np.sum(particles.velocity[:,:2]**2, axis=1) * 0.5 * particles.mass
    #
    # escapees_condition1_3d = (potential_energy + kinetic_energy_3d).number > 0
    # escapees_condition1_2d = (potential_energy + kinetic_energy_2d).number > 0
    #

    #
    # print "Escape velocity"
    # print np.sum(escapees_condition4_3d)
    # print np.sum(escapees_condition4_2d)
    #
    # print "Kinetic energy"
    # print np.sum(escapees_condition1_3d)
    # print np.sum(escapees_condition1_2d)

    escapees_condition1_3d = escape_velocity(particles)
    escapees_condition1_2d = escape_velocity(particles, two_D=True)

    escapees_condition2_3d = find_half_mass_radius_escapees(particles)
    escapees_condition2_2d = find_half_mass_radius_escapees(particles, two_D=True)

    escapees_condition3_3d = radial_and_tangent_velocity(particles.position.number, particles.velocity.number)
    escapees_condition3_2d = radial_and_tangent_velocity(particles.position.number[:,:2], particles.velocity.number[:,:2])

    print "Total energy escapees: ", np.sum(escapees_condition1_3d)
    print "Half mass radius escapees: ", np.sum(escapees_condition2_3d)
    print "Rad Tan velocity escapees:", np.sum(escapees_condition3_3d)

    escapees_3d = (escapees_condition1_3d.astype(int) +
                   escapees_condition2_3d.astype(int) +
                   escapees_condition3_3d.astype(int))

    escapees_2d = (escapees_condition1_2d.astype(int) +
                   escapees_condition2_2d.astype(int) +
                   escapees_condition3_2d.astype(int))

    escapees_3d = escapees_3d[escapees_3d == 3] / 3
    escapees_2d = escapees_2d[escapees_2d == 3] / 3

    # print "The number of escaping stars:", escapees_condition1#  + escapees_condition2) #+ escapees_condition3)

    return escapees_3d, escapees_2d


def escape_velocity(particles, two_D=False):

    total_mass = np.sum(particles.mass.number)

    if two_D:  # When 2d only look at x and y coordinates
        radial_distance_particles = np.sum(particles.position.number[:,:2]**2, axis=1)**0.5
        absolute_velocity = np.sum(particles.velocity.number[:,:2]**2, axis=1)**0.5
    else:
        radial_distance_particles = np.sum(particles.position.number**2, axis=1)**0.5
        absolute_velocity = np.sum(particles.velocity.number**2, axis=1)**0.5

    escape_velocity_particles = (2 * constants.G.number * total_mass / radial_distance_particles)**0.5

    return absolute_velocity > escape_velocity_particles


def find_half_mass_radius_escapees(particles, two_D=False):
    """
    Finds the radius in which half of the total mass of the cluster is contained.  
    Then returns an array of bools for every star indicating if they are inside or outside 
    that radius * 2. 
    """

    if two_D:  # When 2d only look at x and y coordinates
        radial_distance_particles = np.sum(particles.position.number[:,:2]**2, axis=1)**0.5
    else:
        radial_distance_particles = np.sum(particles.position.number**2, axis=1)**0.5

    total_mass = particles.mass.number.sum()
    star_masses = particles.mass.number
    inner_mass = 0
    half_mass_radius = 1e16
    while inner_mass <= 0.5 * total_mass:
        inner_mass = np.sum(star_masses[radial_distance_particles < half_mass_radius])
        half_mass_radius += 1e14

    # print "Mass radius stuff: (inner, total)"
    # print inner_mass, total_mass
    # print "The half mass radius of the cluster: ", half_mass_radius, " m"

    return radial_distance_particles > (half_mass_radius * 2)


def radial_and_tangent_velocity(position, velocity):
    """
    Returns a list of bools, True if the radial velocity is larger than the tangential velocity. 
    """

    normalized_position_vector = position / (np.sum(position**2, axis=1)**0.5)[:, None]

    absolute_velocity_squared = np.sum(velocity**2, axis=1)
    # Radial velocity is the dot product of the normalized position vector and the velocity
    radial_velocity = np.sum(velocity * normalized_position_vector, axis=1)
    # Tangential velocity is the "rest" determined with pythagoras
    tangent_velocity = (absolute_velocity_squared - radial_velocity**2)**0.5

    return np.abs(radial_velocity) > tangent_velocity



        #
    # radial_position_vector = (np.array([particles.x.number**2, particles.y.number, particles.z.number]) /
    #                     np.sum(particles.position.number**2, axis=1) ** 0.5)
    #
    # absolute_velocity = np.sum(particles.velocity.number**2, axis=1)**0.5
    #
    # radial_velocity = np.sum(radial_position_vector * np.array((particles.vx.number, particles.vy.number, particles.vz.number)), axis=0)
    #
    # tangent_velocity = (absolute_velocity**2 - radial_velocity**2)**0.5
    #
    # print "Tangent:", tangent_velocity.shape
    # print "Radial velocity:", radial_velocity.shape
    # print np.sum(tangent_velocity < radial_velocity)
    # return tangent_velocity < radial_velocity



# def radial_and_tangent_velocity_3d(x, y, z, vx, vy, vz):
#
#     pos_vec_norm = np.array([x, y, z]) / (x**2 + y**2 + z**2)
#
#     v_abs = vx**2 + vy**2 + vz**2
#
#     v_rad = np.sum(np.array([vx, vy, vz]) * pos_vec_norm, axis=0)
#
#     v_tan = (v_abs - v_rad**2)**0.5
#
#     print v_rad, v_tan
#
#     return v_rad > v_tan
#
#
# def radial_and_tangent_velocity_2d(x, y, vx, vy):
#
#     pos_vec_norm = np.array([x, y**2]) / (x**2 + y**2)
#
#     v_abs = vx ** 2 + vy ** 2
#
#     v_rad = np.sum(np.array([vx, vy]) * pos_vec_norm, axis=0)
#
#     v_tan = (v_abs - v_rad**2)**0.5
#
#     return v_rad > v_tan