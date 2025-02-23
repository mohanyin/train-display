import logging
from display_connector import interface
from PIL import Image

logging.basicConfig(level=logging.DEBUG)

epd = interface.EPD()

def init():
    logging.info("init and clear")
    epd.init()
    epd.clear()

def display_image(path):
    try:
        logging.info("displaying image")
        # read bmp file 
        with Image.open(path) as image:
            epd.display(epd.getbuffer(image))
        
    except IOError as e:
        logging.info(e)
        exit()


def cleanup():
    epd.sleep()
    interface.epdconfig.module_exit(cleanup=True)