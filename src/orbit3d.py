from orbit2d import *


class Orbit2DOrientation:
    """Orbit2DOrientation is a builder class for the Orbit3D objects."""

    def __init__(self, longitude_node, inclination, periastron_angle):
        """Set orbit's orientation of binary system in 3D space.

        Parameters
        ----------
        longitude_node : float
            The position angle of the ascending node. Expressed in degrees.
        inclination : float
            The orbital inclination between 0 and 180. For inclination < 90
            an object moves in direction of increasing position angle. For
            inclination > 90 the direction is opposite. Expressed in degrees.
        periastron_angle : float
           The angle between the node and the periastron, measured in the
           direction of the motion of the object. Expressed in degrees.
        """
        self.longitude_node = longitude_node
        self.inclination = inclination
        self.periastron_angle = periastron_angle


class Orbit3D(Orbit2D):

    def __init__(self, orbit2d, orientation):
        Orbit2D.__init__(self, orbit2d)
        self.longitude_node = orientation.longitude_node
        self.inclination = orientation.inclination
        self.periastron_angle = orientation.periastron_angle
