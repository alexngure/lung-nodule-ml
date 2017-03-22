import os
import dicom
import xml.etree.ElementTree as ET
from PIL import Image

import Point
import Contour
import Nodule
import LungImage

def print_image(im,dest):
    """
    Takes a LungImage im and outputs a png to dest.
    """
    return

def show_image(im):
    """
    Takes a LungImage im and presents it as a png in a modal view.
    """
    return

def extract_nodules(src):
    """
    Parses and LIDC xml file src and returns the list of Nodules found
    """
    return

def outline_nodules(im,dest,sep=True):
    """
    Draws a border around each nodule in LungImage im and outputs the 
    resulting png to dest. By default, the method will output a
    separate image for each Nodule in im. Set sep=False to create a single 
    image.
    """
    return

def fill_nodules(im,dest,sep=True):
    """
    Fills each Nodule found in im and outputs the resulting png to dest. By default, 
    the method will output separate image for each Nodule in im. Set sep=False 
    to create a single image.
    """
    return

def process_study(src):
    """
    Returns a dictionary of (Image SOP UID,filepath) key-value pairs for every 
    DICOM image in study src
    """
    if not os.path.isdir(src):
        return
    dcm_map = {}
    for root,dirs,files in os.walk(src):
        for file in files:
            file_ext = file.split('.')[1]
            if file_ext == 'dcm':
                filepath = os.path.join(root,file)
                dcmfile = dicom.read_file(filepath)
                dcm_map[dcmfile.SOPInstanceUID] = filepath
    return dcm_map













