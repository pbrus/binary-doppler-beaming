#!/usr/bin/env python3

import numpy as np
from bidobe.orbit import *
from bidobe.plotorb import *


mass1 = 1.0
mass2 = 0.2
sum_major_axis = 1.5e11
eccentricity = 0.397
longitude_node = 80.9
inclination = 47.3
periastron_argument = 130.9

parameters1 = Orbit2DParameters(mass1, mass2, sum_major_axis, eccentricity)
orientation1 = Orbit2DOrientation(longitude_node, inclination,
    periastron_argument)
parameters2 = Orbit2DParameters(mass2, mass1, sum_major_axis, eccentricity)
orientation2 = Orbit2DOrientation(longitude_node + 180, inclination,
    periastron_argument)
orbit1 = Orbit3D(parameters1, orientation1)
orbit2 = Orbit3D(parameters2, orientation2)

period = int(orbit1.period)
time_step = period/5000

orbit1_position = np.empty((1,2), dtype=float)
orbit2_position = np.empty((1,2), dtype=float)
orbit1_velocity = np.empty([])
orbit2_velocity = np.empty([])


for t in np.arange(0.0, period, time_step):
    orbit1.update(t)
    orbit2.update(t)
    x, y = orbit1.projected_position
    orbit1_position = np.append(orbit1_position, np.array([[x, y]]), axis=0)
    x, y = orbit2.projected_position
    orbit2_position = np.append(orbit2_position, np.array([[x, y]]), axis=0)

orbit1_position = orbit1.convert_m_to_au(orbit1_position[1:])
orbit2_position = orbit2.convert_m_to_au(orbit2_position[1:])

plot_projected_orbits(orbit1_position, orbit2_position)
