from math import sqrt, pi, pow, radians, sin, cos
from scipy.optimize import fsolve
from numpy import arcsin
from astro_units import *


class Orbit2D(UnitsConverter):

    def __init__(self, first_mass, second_mass,
                 semi_major_axis, eccentricity, perihelion_passage=0.0):
        self.first_mass = first_mass
        self.second_mass = second_mass
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
        self.perihelion_passage = perihelion_passage

    def calculate_period(self):
        sum_mass = self.first_mass + self.second_mass
        self.period = sqrt(
            4*pow(pi,2)*pow(self.semi_major_axis, 3)
            /(G_unit*(self.convert_sun_mass_to_kg(sum_mass))))

        return self.period

    def calculate_mean_anomaly(self, time):
        self.mean_anomaly = 2*pi*(time - self.perihelion_passage)/self.period

        return self.mean_anomaly

    def calculate_eccentric_anomaly(self):
        self.solve_kepler_equation()

        return self.eccentric_anomaly

    def solve_kepler_equation(self):
        self.eccentric_anomaly = fsolve(lambda x:
            self.mean_anomaly + self.eccentricity*sin(x) - x, 0.0)[0]

        return self.eccentric_anomaly

    def calculate_true_anomaly(self):
        sin_true_anomaly = sqrt(1
            - pow(self.eccentricity, 2))*sin(self.eccentric_anomaly)/(1
            - self.eccentricity*cos(self.eccentric_anomaly))

        self.true_anomaly = arcsin(sin_true_anomaly)

        return self.true_anomaly

    def calculate_distance(self):
        semilatus_rectum = self.semi_major_axis*(1 - pow(self.eccentricity,2))
        self.distance = semilatus_rectum/(1
            + self.eccentricity*cos(self.true_anomaly))

        return self.distance

    def calculate_position(self):
        x_coorindate = self.distance*cos(self.true_anomaly)
        y_coorindate = self.distance*sin(self.true_anomaly)
        self.position = x_coorindate, y_coorindate

        return self.position
