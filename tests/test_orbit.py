"""
Test package of the bidobe.orbit module
"""
import unittest
from bidobe.orbit import *


class Orbit2DTest(unittest.TestCase):

    def setUp(self):
        self.builder = Orbit2DParameters(1.2, 3.5, 2e12, 0.57)
        self.orbit = Orbit2D(self.builder)
        self.orbit.update(875245.0)

    def test_semi_major_axis(self):
        self.orbit.calculate_semi_major_axis()
        self.assertAlmostEqual(self.orbit.semi_major_axis, 1489361702127.6594,
                               delta=0.01)

    def test_period(self):
        period = self.orbit.convert_sec_to_days(self.orbit.period)
        self.assertAlmostEqual(period, 8235.967214572885)

    def test_anomalies(self):
        self.assertAlmostEqual(self.orbit.mean_anomaly, 0.00772824986915738)
        self.assertAlmostEqual(self.orbit.eccentric_anomaly, 0.017971391803595)
        self.assertAlmostEqual(self.orbit.true_anomaly, 0.034337314455718596)

    def test_distance(self):
        distance = self.orbit.convert_m_to_au(self.orbit.distance)
        self.assertAlmostEqual(distance, 4.281921556412359)

    def test_position(self):
        x_position = self.orbit.convert_m_to_sun_radius(self.orbit.position[0])
        y_position = self.orbit.convert_m_to_sun_radius(self.orbit.position[1])
        self.assertAlmostEqual(x_position, 920.2027139943946)
        self.assertAlmostEqual(y_position, 31.609714086772936)

    def test_velocity(self):
        x_speed = self.orbit.convert_mps_to_kmps(self.orbit.velocity[0])
        y_speed = self.orbit.convert_mps_to_kmps(self.orbit.velocity[1])
        self.assertAlmostEqual(x_speed, -0.855053610163753)
        self.assertAlmostEqual(y_speed, 39.08849308032633)

    def tearDown(self):
        self.builder = None
        self.orbit = None


class Orbit3DTest(unittest.TestCase):

    def setUp(self):
        self.builder2d = Orbit2DParameters(1.1, 2.4, 1.3e13, 0.14)
        self.builder3d = Orbit2DOrientation(34.5, 51.9, 170.3)
        self.orbit2d = Orbit2D(self.builder2d)
        self.orbit3d = Orbit3D(self.orbit2d, self.builder3d)
        self.orbit3d.update(357842.23)

    def test_projected_position(self):
        x_position = self.orbit3d.convert_m_to_au(
            self.orbit3d.projected_position[0])
        y_position = self.orbit3d.convert_m_to_au(
            self.orbit3d.projected_position[1])
        self.assertAlmostEqual(x_position, 24.227207640295155)
        self.assertAlmostEqual(y_position, -44.644945462726724)

    def test_radial_velocity(self):
        radial_velocity = self.orbit3d.convert_mps_to_kmps(
            self.orbit3d.radial_velocity)
        self.assertAlmostEqual(radial_velocity, -3.6606298593886395)

    def tearDown(self):
        self.builder2d = None
        self.builder3d = None
        self.orbit2d = None
        self.orbit3d = None
