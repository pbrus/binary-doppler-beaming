from math import sqrt, pi, pow, radians
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

        if hasattr(self, "period") == False:
            self.period = sqrt(
                4*pow(pi,2)*pow(self.semi_major_axis, 3)
                /(G_unit*(self.convert_sun_mass_to_kg(sum_mass))))

        return self.period

    def calculate_mean_anomaly(self, time):
        if hasattr(self, "mean_anomaly") == False:
            self.mean_anomaly = 2*pi*(time - self.perihelion_passage)
                                /self.period

        return self.mean_anomaly

    def calculate_eccentric_anomaly(self):
        self.solve_kepler_equation()
        return self.eccentric_anomaly

    def solve_kepler_equation(self):
        pass
