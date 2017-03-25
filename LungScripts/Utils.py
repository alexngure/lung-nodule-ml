import os
import dicom
import xml.etree.ElementTree as ET
from PIL import Image


class ROI(object):
    """A non-flatbuffers implementation of the Contour class. Created
    primarily to hold the Nodule information returned from the xml
    processing function where we're not really using any flatbuffer
    functionality, but still need a clean way to represent this information.
    """
    def __init__(self, image_UID,inclusion,contour):
        self._image_UID = image_UID
        self._inclusion = inclusion
        self._contour = contour

    def image_UID():
        return self._image_UID

    def inclusion():
        return self._inclusion

    def contour():
        return self._contour

class Characteristics(object):
    """A class to hold a Nodule's characteristic information"""
    def __init__(self):
        self._subtlety           = -1
        self._internal_structure = -1
        self._calcification      = -1
        self._sphericity         = -1
        self._margin             = -1
        self._lobulation         = -1
        self._spiculation        = -1
        self._texture            = -1
        self._malignancy         = -1

    def set_subtlety(val):
        self._subtlety = val

    def set_internal_structure(val):
        self._internal_structure = val

    def set_calcification(val):
        self._calcification = val

    def set_sphericity(val):
        self._sphericity = val

    def set_margin(val):
        self._margin = val

    def set_lobulation(val):
        self._lobulation = val

    def set_spiculation(val):
        self._spiculation = val

    def set_texture(val):
        self._texture = val

    def set_malignancy(val):
        self._malignancy = val

    def subtlety():
        return self._subtlety
    def internal_structure():
        return self._internal_structure
    def calcification():
        return self._calcification

    def sphericity():
        return self._sphericity

    def margin():
        return self._margin

    def lobulation():
        return self._lobulation

    def spiculation():
        return self._spiculation

    def texture():
        return self._texture

    def malignancy():
        return self._malignancy

class Nodule(object):
    """A non-flatbuffers implementation of the Nodule class.
    """
    def __init__(self, nodule_id):
        self._noduleID = nodule_id
        self._characteristics = Characteristics()
        self._roi_list = []

    def noduleID():
        return self._noduleID

    def characteristics():
        return self._characteristics

    def addCharacteristics(characteristics_):
        self._characteristics = characteristics_

    def addROI(roi_):
        self._roi_list.append(roi_)

def print_image(im,dest):
    """Takes a LungImage im and outputs a png to dest."""
    return

def show_image(im):
    """Takes a LungImage im and presents it as a png in a modal view."""
    return

def extract_nodules(src):
    """Parses an LIDC xml file src and returns the list of Nodules found"""
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
        nodule = Nodule(nodule_id)
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
            char_object        = Characteristics()
            char_object.set_subtlety(int(subtlety))
            char_object.set_internal_structure(int(internal_structure))
            char_object.set_calcification(int(calcification))
            char_object.set_sphericity(int(sphericity))
            char_object.set_margin(int(margin))
            char_object.set_lobulation(int(lobulation))
            char_object.set_spiculation(int(spiculation))
            char_object.set_texture(int(texture))
            char_object.set_malignancy(int(malignancy))
            nodule.addCharacteristics(char_object)
        for roi in session.findall(roi_key):
            image_UID = roi.find(image_UID_key).text
            inclusion = roi.find(inclusion_key)
            roi_outline   = []
            for point in roi.findall(edgemap_key):
                x_coord = point.find(x_coord_key).text
                y_coord = point.find(y_coord_key).text
                roi_outline.append((int(x_coord),int(y_coord)))
    return nodule_list

def outline_nodules(im,dest,sep=True):
    """Draws a border around each nodule in LungImage im and outputs the
    resulting png to dest. By default, the method will output a
    separate image for each Nodule in im. Set sep=False to create a single
    image.
    """
    return

def fill_nodules(im,dest,sep=True):
    """Fills each Nodule found in im and outputs the resulting png to dest. By default,
    the method will output separate image for each Nodule in im. Set sep=False
    to create a single image.
    """
    return

def process_study(src):
    """Returns a dictionary of (Image SOP UID,filepath) key-value pairs for every
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
