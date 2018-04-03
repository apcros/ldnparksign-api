from PIL import Image
import pytesseract
import cv2
import calendar
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

        self.image_string = text;
        parsed_data = self._parse_string(text)
        print(parsed_data)
        return text

    @staticmethod
    def _crop_picture(image):
         width = len(image[0])
         height = len(image[1])
         #TODO : Detect the parking sign area and crop it
         return image[200:450, 325:600]

    # Because OCR parsing is, by definition, really flaky we need
    # to include a maximum of safe guards in this parsing method
    @staticmethod
    def _parse_string(image_string):
        parking_infos = {
            'ranges' : [],
            'single_days': []
        }

        # London parking signs use alternatively short and long names
        days = list(calendar.day_abbr) + list(calendar.day_name)

        matched_days = {}
        for day in days:
            match = image_string.find(day)

            if match != -1 and match not in matched_days:
                matched_days[match] = day

        print(matched_days)

        CHAR_COUNT_IN_SEP = 3

        for index, match_index in enumerate(matched_days):
            print(index)

            next_index = index + 1

            day_name = matched_days[index].items()[0]
            print(day_name)

            if next_index >= len(matched_days):
                parking_infos['single_days'].append(({
                    'day': day_name
                }))
                continue

            if match_index + CHAR_COUNT_IN_SEP + len(day_name) == matched_days.get(next_index).items()[0]:
                parking_infos['ranges'].append({
                    'from': {
                        'day': day_name,
                        'time': ''
                    },
                    'to': {
                        'day': matched_days[index+1],
                        'time': ''
                    }
                })
                # We just found a day range


        print(parking_infos)
        print(matched_days)
        return parking_infos



