from PIL import Image
import pytesseract
import cv2
import calendar
import tempfile
import os
import numpy
import imutils

class ParkingSignParser:

    def __init__(self, filename):
        self.filename = filename
        self.LOWER_GRAY_BOUND = 125
        self.MIN_NUM_OF_PIX_IN_MASK = 35

    def save_temp_image(self, image, name='def'):
        base_path = '/Users/apcros/Desktop/sign/'
        base_filename = self.filename.split('/')[-1]

        temp_filename = '{}{}-{}'.format(base_path, name, base_filename)
        cv2.imwrite(
            temp_filename,
            image
        )

        return temp_filename

    def image_to_string(self):
        image = cv2.imread(self.filename)
        gray_scale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        self.save_temp_image(gray_scale_image, 'gray')
        gray_scale_image = self.detect_sign_and_crop_picture(gray_scale_image)
        self.save_temp_image(gray_scale_image, 'croped')
        gray_scale_image = cv2.threshold(gray_scale_image, self.LOWER_GRAY_BOUND, 255, cv2.THRESH_TOZERO | cv2.THRESH_BINARY)[1]
        #gray_scale_image = cv2.medianBlur(gray_scale_image, 1)
        
        temp_file_name = self.save_temp_image(gray_scale_image, 'pre-ocr')

        text = pytesseract.image_to_string(Image.open(temp_file_name))
        print("====== IMAGE TO STRING ====")
        print(text)
        print("===== IMAGE/ ======")
        #temp_file.close()
        #os.remove(temp_file_name)

        self.image_string = text;
        parsed_data = self._parse_string(text)
        print(parsed_data)
        return text

    def detect_sign_and_crop_picture(self, image):
        width = len(image[0])
        height = len(image[1])

        lower = numpy.array([self.LOWER_GRAY_BOUND])
        upper = numpy.array([255])
        shapeMask = cv2.inRange(image, lower, upper)
        self.save_temp_image(shapeMask, 'sign-mask')
        print(shapeMask)

        cnts = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        # loop over the contours
        xs = []
        ys = []

        for c in cnts:
            # draw the contour and show it
            if len(c) > self.MIN_NUM_OF_PIX_IN_MASK:
                print("FOUND ONE ({})".format(len(c)))
                sorted_c = sorted(c, key=lambda x: (x[0][0], x[0][1]) )
                first_elem = sorted_c[0][0]
                last_elem = sorted_c[-1][0]

                xs.append(first_elem[0])
                xs.append(last_elem[0])

                ys.append(first_elem[1])
                ys.append(last_elem[1])

        
        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)
        print("{}:{} {}:{}".format(min_x, max_x, min_y, max_y))
        return image[min_x:max_x, min_y:max_y]


    @staticmethod
    def parse_image_string():
        pass
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



