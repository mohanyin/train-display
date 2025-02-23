import logging
from display_connector import interface
from PIL import Image


class DisplayConnector:
    def __init__(self):
        self.epd = interface.EPD()
        logging.basicConfig(level=logging.DEBUG)


    def init(self):
        logging.info("init and clear")
        self.epd.init()
        self.epd.clear()
        

    def display_image(self, path):
        try:
            logging.info("displaying image")
            # read bmp file 
            with Image.open(path) as image:
                self.epd.display(self.epd.getbuffer(image))
            
        except IOError as e:
            logging.warning(e)
            exit()


    def cleanup(self):
        self.epd.sleep()
        interface.epdconfig.module_exit(cleanup=True)