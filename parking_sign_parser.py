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
        gray_scale_image = cv2.threshold(gray_scale_image, 150, 255, cv2.THRESH_OTSU)[1]
        #temp_file = tempfile.TemporaryFile()
        temp_file_name = '/tmp/test.png';
        cv2.imwrite(temp_file_name, gray_scale_image)

        text = pytesseract.image_to_string(Image.open(temp_file_name))
        #temp_file.close()
        #os.remove(temp_file_name)

        return text
