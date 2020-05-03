import unittest
import os

from parking_sign_parser import ParkingSignParser


class TestParkingSignParser(unittest.TestCase):

    def test_image_to_string(self):

        # OpenCV needs the full path
        sign_parser = ParkingSignParser(os.getcwd()+'/tests/fixtures/sign-1.png')
        text_2 = ParkingSignParser(os.getcwd()+'/tests/fixtures/sign-2.png').image_to_string()
        text_3 = ParkingSignParser(os.getcwd()+'/tests/fixtures/sign-3.png').image_to_string()

        self.assertEquals(sign_parser.image_to_string(), 'Super test')
