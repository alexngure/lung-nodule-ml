import cv2
import os
import dicom
import xml.etree.ElementTree as ET
import OSS.pydicom_PIL as pdp
from PIL import Image,ImageColor,ImageDraw

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

    def image_UID(self):
        return self._image_UID

    def inclusion(self):
        return self._inclusion

    def contour(self):
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

    def set_subtlety(self,val):
        self._subtlety = val

    def set_internal_structure(self,val):
        self._internal_structure = val

    def set_calcification(self,val):
        self._calcification = val

    def set_sphericity(self,val):
        self._sphericity = val

    def set_margin(self,val):
        self._margin = val

    def set_lobulation(self,val):
        self._lobulation = val

    def set_spiculation(self,val):
        self._spiculation = val

    def set_texture(self,val):
        self._texture = val

    def set_malignancy(self,val):
        self._malignancy = val

    def subtlety(self):
        return self._subtlety

    def internal_structure(self):
        return self._internal_structure

    def calcification(self):
        return self._calcification

    def sphericity(self):
        return self._sphericity

    def margin(self):
        return self._margin

    def lobulation():
        return self._lobulation

    def spiculation(self):
        return self._spiculation

    def texture(self):
        return self._texture

    def malignancy(self):
        return self._malignancy

class Nodule(object):
    """A non-flatbuffers implementation of the Nodule class."""
    def __init__(self, nodule_id):
        self._noduleID = nodule_id
        self._characteristics = Characteristics()
        self._roi_list = []

    def noduleID(self):
        return self._noduleID

    def characteristics(self):
        return self._characteristics

    def ROI_list(self):
        return self._roi_list

    def addCharacteristics(self,characteristics_):
        self._characteristics = characteristics_

    def addROI(self,roi_):
        self._roi_list.append(roi_)

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
        nodule = Nodule(nodule_id)

        characteristics = session.find(characteristics_key)
        if characteristics is not None and len(characteristics) > 0:
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
        else:
            nodule.addCharacteristics(None)

        for roi in session.findall(roi_key):
            roi_outline   = []
            for point in roi.findall(edgemap_key):
                x_coord = point.find(x_coord_key).text
                y_coord = point.find(y_coord_key).text
                roi_outline.append((int(x_coord),int(y_coord)))
            image_UID = roi.find(image_UID_key).text
            inclusion = roi.find(inclusion_key).text
            if inclusion == 'TRUE':
                inclusion = True
            else:
                inclusion = False
            roi_object = ROI(image_UID,inclusion,roi_outline)
            nodule.addROI(roi_object)
        nodule_list.append(nodule)
    return nodule_list

def process_study(src):
    """Returns a dictionary of (Image SOP UID,filepath) key-value pairs for every
    DICOM image in study src
    """
    dcm_map = {}
    if not os.path.isdir(src):
        return dcm_map
    for root,dirs,files in os.walk(src):
        for file in files:
            file_ext = file.split('.')[1]
            if file_ext == 'dcm':
                filepath = os.path.join(root,file)
                dcmfile = dicom.read_file(filepath)
                dcm_map[dcmfile.SOPInstanceUID] = filepath
    return dcm_map

def outline_nodule(dcm,contour,dest,color='red'):
    """Takes DICOM file dcm, overlays the contour (list of (x,y) cordinates) and
    outputs the resulting image to dest.
    """
    color = ImageColor.getrgb(color)
    dataset = dicom.read_file(dcm)
    im = pdp.get_image(dataset)
    im = im.convert('RGB')
    draw = ImageDraw.Draw(im)
    draw.line(contour,color)
    im.save(dest)
    return

def get_image(dcm):
    """Takes DICOM file dcm and returns its pixel data
     as a PIL image object
     """
    dataset = dicom.read_file(dcm)
    im = pdp.get_image(dataset)
    return im

def print_image(dcm,dest):
    """Takes DICOM file dcm and outputs its pixel data to dest as an image."""
    im = get_image(dcm)
    im.save(dest)
    return

def show_image(dcm):
    """Takes DICOM file dcm and presents it as a png in a modal view."""
    im = get_image(dcm)
    im.show()
    return

def fill_nodule(dcm,countour,dest,color='red'):
    """Takes DICOM file dcm, fills the region outlined by countour (list of (x,y)
    coordinates), and outputs the resulting image to dest.
    """
    return

def segment_lung(dcm):
    """Takes chest CT scan as DICOM file dcm and returns an image
    containing the segmented lung area.
    """
    ds = dicom.read_file(dcm)
    hu_array = ds.pixel_array*ds.RescaleSlope + ds.RescaleIntercept
    ret,thresh = cv2.threshold(hu_array,-480,255,cv2.THRESH_BINARY)
    thresh_filled = thresh.astype(np.uint8)
    h,w = thresh_filled.shape[:2]
    mask = np.zeros((h+2,w+2),np.uint8)
    cv2.floodFill(thresh_filled,mask,(0,0),255)
    kernel = np.zeros((3,3),np.uint8)
    img_dilated = cv2.dilate(thresh_filled,kernel)
    image = pdp.get_LUT_value(hu_array,ds.WindowWidth,ds.WindowCenter).astype(np.uint32)
    x = image | img_dilated
    x = np.piecewise(x,[x == 255, x < 255], [lambda x : 0, lambda x: x])
    lung_img = PIL.Image.fromarray(x).convert('L')
    return lung_img
