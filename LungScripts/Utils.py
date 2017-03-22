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
    xmlns                     = "{http://www.nih.gov}"
    read_session_key          = xmlns + "unblindedReadNodule"
    nodule_ID_key             = xmlns + "noduleID"
    characteristics_key       = xmlns + "characteristics"
    roi_key                   = xmlns + "roi"
    image_UID_key             = xmlns + "imageSOP_UID"
    inclusion_key             = xmlns + "inclusion"
    edgemap_key               = xmlns + "edgeMap"
    x_coord_key               = xmlns + "xCoord"
    y_coord_key               = xmlns + "yCoord"
    ch_subtlety_key           = xmlns + "subtlety"
    ch_internal_structure_key = xmlns + "internalStructure"
    ch_calcification_key      = xmlns + "calcification"
    ch_sphericity_key         = xmlns + "sphericity"
    ch_margin_key             = xmlns + "margin"
    ch_lobulation_key         = xmlns + "lobulation"
    ch_spiculation_key        = xmlns + "spiculation"
    ch_texture_key            = xmlns + "texture"
    ch_malignancy_key         = xmlns + "malignancy"
    
    xml_tree      = ET.parse(src)
    read_sessions = xml_tree.getroot().iter(read_session_key)
    nodule_list   = [] 
    
    for session in read_sessions:
        nodule_id       = session.find(nodule_ID_key).text
        characteristics = session.find(characteristics_key) 
        if characteristics is not None:
            subtlety           = characteristics.find(ch_subtlety_key).text
            internal_structure = characteristics.find(ch_internal_structure_key).text
            calcification      = characteristics.find(ch_calcification_key).text
            sphericity         = characteristics.find(ch_sphericity_key).text
            margin             = characteristics.find(ch_margin_key).text
            lobulation         = characteristics.find(ch_lobulation_key).text
            spiculation        = characteristics.find(ch_spiculation_key).text
            texture            = characteristics.find(ch_texture_key).text
            malignancy         = characteristics.find(ch_malignancy_key).text
    return nodule_list

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













