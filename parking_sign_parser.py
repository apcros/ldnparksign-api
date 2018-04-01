from PIL import Image
import pytesseract
import cv2
import tempfile
import os


class ParkingSignParser:

    def __init__(self, filename):
        self.filename = filename

    def image_to_string(self):
        image = cv2.imread(self.filename)
        gray_scale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_scale_image = self._crop_picture(gray_scale_image)
        gray_scale_image = cv2.threshold(gray_scale_image, 200, 255, cv2.THRESH_TOZERO | cv2.THRESH_BINARY)[1]
        gray_scale_image = cv2.medianBlur(gray_scale_image, 3)
        print(len(gray_scale_image[0]))
        #temp_file = tempfile.TemporaryFile()
        temp_file_name = '/tmp/test.png';
        cv2.imwrite(temp_file_name, gray_scale_image)

        text = pytesseract.image_to_string(Image.open(temp_file_name))
        print(text)
        #temp_file.close()
        #os.remove(temp_file_name)

        parsed_data = self._parse_string(text)
        print(parsed_data)
        return text

    @staticmethod
    def _crop_picture(image):
         width = len(image[0])
         height = len(image[1])
         #TODO : Detect the parking sign area and crop it
         return image[200:450, 325:600]

    @staticmethod
    def _parse_string(image_string):
        parking_infos = {}
        
        return parking_infos
