"""
Test package of the bidobe.dobe module
"""
import unittest
from bidobe.dobe import *


class OrbitingObjectTest(unittest.TestCase):

    def setUp(self):
        self.orbiting_object = OrbitingObject(763.3, 1.2, 6750, "B")

    def test_stationary_flux(self):
        self.assertAlmostEqual(self.orbiting_object.flux,
            1.4785989393228895e-13, delta=1e-12)

    def test_alpha_parameter(self):
        self.assertAlmostEqual(self.orbiting_object.alpha, -1.8828083664327906)

    def test_doppler_coefficient(self):
        doppler_coefficient = (
            self.orbiting_object.calculate_doppler_coefficient(1435.24))
        self.assertAlmostEqual(doppler_coefficient, 1.000023376178062)

    def tearDown(self):
        self.orbiting_object = None


class BinaryBrightnessTest(unittest.TestCase):

    def setUp(self):
        self.distance = 342.5
        self.passband = "V"
        self.velocity = 23500
        self.first_object = OrbitingObject(self.distance, 0.8, 5500,
            self.passband)
        self.second_object = OrbitingObject(self.distance, 1.2, 6920,
            self.passband)
        self.first_object.calculate_doppler_coefficient(self.velocity)
        self.second_object.calculate_doppler_coefficient(self.velocity)

    def test_binary_brightness(self):
        brightness = binary_brightness(self.first_object, self.second_object)
        self.assertAlmostEqual(brightness, 16.000341102118394, delta=1e-10)

    def tearDown(self):
        self.distance = None
        self.passband = None
        self.velocity = None
        self.first_object = None
        self.second_object = None
