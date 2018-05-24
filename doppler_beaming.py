#!/usr/bin/env python3

from bidobe.orbit import *


mass1 = 6.0
mass2 = 0.8
sum_major_axis = 5e8
eccentricity = 0.9
longitude_node = 40
inclination = 40.0
periastron_argument = 30

parameters1 = Orbit2DParameters(mass1, mass2, sum_major_axis, eccentricity)
orientation1 = Orbit2DOrientation(longitude_node, inclination,
    periastron_argument)
parameters2 = Orbit2DParameters(mass2, mass1, sum_major_axis, eccentricity)
orientation2 = Orbit2DOrientation(longitude_node + 180, inclination,
    periastron_argument)
orbit1 = Orbit3D(parameters1, orientation1)
orbit2 = Orbit3D(parameters2, orientation2)

period = int(orbit1.period)
time_step = int(period/2000)

for t in range(0, period, time_step):
    orbit1.update(t)
    orbit2.update(t)
    vx1, vy1 = orbit1.velocity
    vx2, vy2 = orbit2.velocity
    x1, y1 = orbit1.projected_position
    x2, y2 = orbit2.projected_position

    print(t, vx1, vx2)
    #print(x1, y1, x2, y2)
