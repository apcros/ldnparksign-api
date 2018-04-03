import unittest
import os

from parking_sign_parser import ParkingSignParser


class TestParkingSignParser(unittest.TestCase):

    def test_image_to_string(self):

        # OpenCV needs the full path
        sign_parser = ParkingSignParser(os.getcwd()+'/fixtures/sign-1.png')

        self.assertEquals(sign_parser.image_to_string(), 'Super test')
