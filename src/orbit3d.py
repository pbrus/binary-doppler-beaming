from math import radians
from orbit2d import *


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

    def update(self, time):
        Orbit2D.update(self, time)
        x, y = self.position
        self.inclination = 0
        x_rot, y_rot = self.rotate_coordinate_system(x, y,
            self.periastron_argument)
        x_sky, y_sky = self.rotate_coordinate_system(x_rot,
            y_rot*cos(self.inclination), self.longitude_node)

        return x_sky, y_sky

    def rotate_coordinate_system(self, x, y, angle):
        x_rotate = x*cos(-angle) + y*sin(-angle)
        y_rotate = -x*sin(-angle) + y*cos(-angle)

        return x_rotate, y_rotate
