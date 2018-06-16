#!/usr/bin/env python3

import numpy as np
import configparser as cfg
from bidobe.orbit import *
from bidobe.plotorb import *
from bidobe.dobe import *


configure_file = "binary.conf"
config = cfg.ConfigParser()

if config.read(configure_file) == []:
    print("There is no {0} file".format(configure_file))
    exit(1)
else:
    mass1 = float(config["OBJECTS"]["mass1"])
    mass2 = float(config["OBJECTS"]["mass2"])
    temperature1 = int(config["OBJECTS"]["temperature1"])
    temperature2 = int(config["OBJECTS"]["temperature2"])
    radius1 = float(config["OBJECTS"]["radius1"])
    radius2 = float(config["OBJECTS"]["radius2"])
    distance = float(config["OBJECTS"]["distance"])
    sum_major_axis = float(config["ORBITS"]["sum_major_axis"])
    eccentricity = float(config["ORBITS"]["eccentricity"])
    longitude_node = float(config["ORBITS"]["longitude_node"])
    inclination = float(config["ORBITS"]["inclination"])
    periastron_argument = float(config["ORBITS"]["periastron_argument"])
    multiply_period_length = float(
        config["OBSERVATION"]["multiply_period_length"])
    time_length_pieces = int(config["OBSERVATION"]["time_length_pieces"])
    passband = config["OBSERVATION"]["passband"]

temperatures = (temperature1, temperature2)
object1 = OrbitingObject(distance, radius1, temperature1, passband)
object2 = OrbitingObject(distance, radius2, temperature2, passband)
parameters1 = Orbit2DParameters(mass1, mass2, sum_major_axis, eccentricity)
orientation1 = Orbit2DOrientation(longitude_node, inclination,
    periastron_argument)
parameters2 = Orbit2DParameters(mass2, mass1, sum_major_axis, eccentricity)
orientation2 = Orbit2DOrientation(longitude_node, inclination,
    periastron_argument + 180)
orbit1 = Orbit3D(parameters1, orientation1)
orbit2 = Orbit3D(parameters2, orientation2)

time_length = multiply_period_length*int(orbit1.period)
time_step = time_length/time_length_pieces
time_range = np.arange(0.0, time_length, time_step, dtype=float)

orbit1_position = np.empty(shape=(0,2), dtype=float)
orbit2_position = np.empty(shape=(0,2), dtype=float)
orbit1_velocity = np.empty(0, dtype=float)
orbit2_velocity = np.empty(0, dtype=float)
brightness = np.empty(0, dtype=float)

for time in time_range:
    orbit1.update(time)
    orbit2.update(time)
    x, y = orbit1.projected_position
    v_rad1 = orbit1.radial_velocity
    orbit1_position = np.append(orbit1_position, np.array([[x, y]]), axis=0)
    orbit1_velocity = np.append(orbit1_velocity, np.array(v_rad1))
    x, y = orbit2.projected_position
    v_rad2 = orbit2.radial_velocity
    orbit2_position = np.append(orbit2_position, np.array([[x, y]]), axis=0)
    orbit2_velocity = np.append(orbit2_velocity, np.array(v_rad2))
    object1.calculate_doppler_coefficient(v_rad1)
    object2.calculate_doppler_coefficient(v_rad2)
    brightness = np.append(brightness, binary_brightness(object1, object2))

orbit1_position = orbit1.convert_m_to_au(orbit1_position)
orbit2_position = orbit2.convert_m_to_au(orbit2_position)
orbit1_velocity = orbit1.convert_mps_to_kmps(orbit1_velocity)
orbit2_velocity = orbit1.convert_mps_to_kmps(orbit2_velocity)
time = orbit1.convert_sec_to_days(time_range)


plot_projected_orbits(orbit1_position, orbit2_position, "AU", "AU")
plot_radial_velocities(time, orbit1_velocity, orbit2_velocity,
    "days", "km/s")
plot_light_curve(time, brightness, "days")
