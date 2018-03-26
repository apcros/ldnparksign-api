import unittest
from parking_sign_parser import ParkingSignParser


class TestParkingSignParser(unittest.TestCase):

    def test_image_to_string(self):
        sign_parser = ParkingSignParser('/home/apcros/PycharmProjects/ldnparksign-api/tests/fixtures/sign-1.png')

        self.assertEquals(sign_parser.image_to_string(), 'Super test')
