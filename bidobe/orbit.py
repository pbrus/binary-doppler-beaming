from math import sqrt, pi, pow, radians, sin, cos, atan2, asin
from scipy.optimize import fsolve
from bidobe.astunit import *


class Orbit2DParameters:
    """Orbit2DParameters is a builder class for the Orbit2D objects."""

    def __init__(self, first_mass, second_mass,
                 separation, eccentricity, periastron_passage=0.0):
        """Set basic parameters of binary system in 2D space.

        Parameters
        ----------
        first_mass, second_mass : float
            Star masses of binary system. Expressed in Sun mass unit.
        separation : float
            Separation between two masses expressed in meters.
        eccentricity : float
            A value of orbit's eccentricity between 0 and 1.
        periastron_passage : float
            A moment when a star passes periastron. Default = 0.
        """
        self.first_mass = first_mass
        self.second_mass = second_mass
        self.separation = separation
        self.eccentricity = eccentricity
        self.periastron_passage = periastron_passage


class Orbit2D(UnitsConverter):
    """Orbit2D represents the position and velocity vectors of any object
    in binary system. For any given time t the: x(t), y(t), v_x(t), v_y(t)
    are computed."""

    def __init__(self, orbit2d):
        self.first_mass = orbit2d.first_mass
        self.second_mass = orbit2d.second_mass
        self.separation = orbit2d.separation
        self.eccentricity = orbit2d.eccentricity
        self.periastron_passage = orbit2d.periastron_passage
        self.calculate_semi_major_axis()
        self.calculate_period()

    def calculate_semi_major_axis(self):
        """Calculate a semi major axis."""
        sum_mass = self.first_mass + self.second_mass
        self.semi_major_axis = self.separation*self.second_mass/sum_mass

        return self.semi_major_axis

    def calculate_period(self):
        """Calculate a period in seconds."""
        sum_mass = self.first_mass + self.second_mass
        self.period = sqrt(
            4*pow(pi,2)*pow(self.separation, 3)
            /(self.G*(self.convert_sun_mass_to_kg(sum_mass))))

        return self.period

    def calculate_mean_anomaly(self, time):
        """Calculate a mean anomaly in radians."""
        self.mean_anomaly = 2*pi*(time - self.periastron_passage)/self.period

        return self.mean_anomaly

    def calculate_eccentric_anomaly(self):
        """Calculate an eccentric anomaly in radians."""
        self.solve_kepler_equation()

        return self.eccentric_anomaly

    def solve_kepler_equation(self):
        self.eccentric_anomaly = fsolve(lambda x:
            self.mean_anomaly + self.eccentricity*sin(x) - x, 0.0)[0]

        return self.eccentric_anomaly

    def calculate_true_anomaly(self):
        """Calculate a true anomaly in radians."""
        x = sqrt(1 - self.eccentricity)*cos(0.5*self.eccentric_anomaly)
        y = sqrt(1 + self.eccentricity)*sin(0.5*self.eccentric_anomaly)
        self.true_anomaly = 2*atan2(y, x)

        if self.true_anomaly < 0:
            self.true_anomaly += 2*pi

        return self.true_anomaly

    def calculate_distance(self):
        """Calculate distance in meters."""
        semilatus_rectum = self.semi_major_axis*(1 - pow(self.eccentricity,2))
        self.distance = semilatus_rectum/(1
            + self.eccentricity*cos(self.true_anomaly))

        return self.distance

    def calculate_position(self):
        """Calculate position tuple in meters."""
        x_coorindate = self.distance*cos(self.true_anomaly)
        y_coorindate = self.distance*sin(self.true_anomaly)
        self.position = x_coorindate, y_coorindate

        return self.position

    def calculate_velocity(self):
        """Calculate velocity tuple in meters per second."""
        speed = self.calculate_speed()
        angle = self.calculate_velocity_angle()
        self.velocity = speed*cos(angle), speed*sin(angle)

        return self.velocity

    def calculate_speed(self):
        sum_mass = self.first_mass + self.second_mass
        speed_pow2 = 2/self.distance - 1/self.semi_major_axis
        speed_pow2 *= self.G*self.convert_sun_mass_to_kg(sum_mass)

        return sqrt(speed_pow2)

    def calculate_velocity_angle(self):
        sin_angle = (pow(self.semi_major_axis, 2)
                     - pow(self.eccentricity*self.semi_major_axis,2))
        sin_angle /= (self.distance*(2*self.semi_major_axis - self.distance))
        sin_angle = sqrt(sin_angle)

        if divmod(self.true_anomaly, 2*pi)[1] <= pi:
            velocity_angle = asin(sin_angle) + self.true_anomaly
        else:
            velocity_angle = pi - asin(sin_angle) + self.true_anomaly

        return velocity_angle

    def update(self, time):
        """Update x, y, v_x, v_y for particular time"""
        self.calculate_mean_anomaly(time)
        self.calculate_eccentric_anomaly()
        self.calculate_true_anomaly()
        self.calculate_distance()
        self.calculate_position()
        self.calculate_velocity()


class Orbit2DOrientation:
    """Orbit2DOrientation is a builder class for the Orbit3D objects."""

    def __init__(self, longitude_node, inclination, periastron_argument):
        """Set orbit's orientation of binary system in 3D space.

        Parameters
        ----------
        longitude_node : float
            The position angle of the ascending node. Expressed in degrees.
        inclination : float
            The orbital inclination between 0 and 180. For inclination < 90
            an object moves in direction of increasing position angle. For
            inclination > 90 the direction is opposite. Expressed in degrees.
        periastron_argument : float
           The angle between the node and the periastron, measured in the
           direction of the motion of the object. Expressed in degrees.
        """
        self.longitude_node = radians(longitude_node)
        self.inclination = radians(inclination)
        self.periastron_argument = radians(periastron_argument)

        if self.inclination < 90.0:
            self.longitude_periapsis = (self.longitude_node
                                        + self.periastron_argument)
        else:
            self.longitude_periapsis = (self.longitude_node
                                        - self.periastron_argument)


class Orbit3D(Orbit2D):

    def __init__(self, orbit2d, orientation):
        Orbit2D.__init__(self, orbit2d)
        self.longitude_node = orientation.longitude_node
        self.inclination = orientation.inclination
        self.periastron_argument = orientation.periastron_argument
        self.longitude_periapsis = orientation.longitude_periapsis

    def rotate_coordinate_system(self, x, y, angle):
        x_rotate = x*cos(-angle) + y*sin(-angle)
        y_rotate = -x*sin(-angle) + y*cos(-angle)

        return x_rotate, y_rotate

    def calculate_projected_position(self):
        x, y = self.position
        x_rot, y_rot = self.rotate_coordinate_system(x, y,
            self.periastron_argument)
        self.projected_position = self.rotate_coordinate_system(x_rot,
            y_rot*cos(self.inclination), self.longitude_node)

        return self.projected_position

    def calculate_velocity(self):
        """Calculate velocity tuple in meters per second."""
        speed = self.calculate_speed()
        angle = (self.calculate_velocity_angle()
            + self.longitude_node + self.periastron_argument)
        self.velocity = speed*cos(angle)*sin(self.inclination), speed*sin(angle)

        return self.velocity

    def update(self, time):
        """Update x, y, v_x, v_y projected on the sky for particular time."""
        Orbit2D.update(self, time)
        self.calculate_projected_position()
        self.calculate_velocity()
