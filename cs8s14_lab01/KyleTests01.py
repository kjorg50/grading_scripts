# Kyle's tests for grading lab01

import math                    # this is so we can use math.pi
import unittest                # this is so we can set up testing of functions
from lab01Funcs import *       # this says: get all the functions from the lab01Funcs file


class KyleTests(unittest.TestCase):   # This is how you do testing in Python

    # Every test case should be a function definition
    # The name should start with test_ and the parameter should be "self".
    # Then, you can write tests using self.assertEqual(actual, expected) and 
    # self.assertAlmostEquals(actual, expected, numberOfDecimalPlaces)
    #
    # If an answer should be exact (e.g. integer math), use assertEqual
    # If an answer is approximate (floating pt math, square roots, pi, etc.)
    #    use assertAlmostEqual


    def test_milesToKm1(self):
        self.assertAlmostEqual(milesToKm(12), 19.3121,2)

    def test_milesToKm2(self):
        self.assertAlmostEqual(milesToKm(9.5), 15.2888,2)

    def test_milesToKm3(self):
        self.assertAlmostEqual(milesToKm(-3.10686), -5,2)

    def test_milesToKm4(self):
        self.assertAlmostEqual(milesToKm(-3), -4.82803, 2)

    

# This code says: when you run this file, run the tests!

if __name__ == '__main__':
    unittest.main(exit=False)
