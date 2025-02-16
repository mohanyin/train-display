import os

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'outputs')

import logging
from display_connector import interface
from PIL import Image

logging.basicConfig(level=logging.DEBUG)

epd = interface.EPD()

def init():
    logging.info("init and Clear")
    epd.init()
    epd.Clear()

def display_image():
    try:
        logging.info("writing image")
        # read bmp file 
        Himage = Image.open(os.path.join(picdir, 'output.png'))
        epd.display(epd.getbuffer(Himage))
        
        logging.info("Goto Sleep...")
        epd.sleep()
            
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        interface.epdconfig.module_exit(cleanup=True)
        exit()
