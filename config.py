import configparser
import os


class Config:

    sections = None

    def __init__(self):
        self.load()

    def load(self):
        mode = os.environ.get('APP_MODE') or 'development'
        config = configparser.ConfigParser()
        sections = config.read('configs/'+mode+'.json').sections()
        self.sections = sections
