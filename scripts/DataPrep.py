import os
import sys
import json
import progressbar

import flatbuffers
import LungData
import LungData.Point as FBPoint
import LungData.RegionOfInterest as FBROI
import LungData.Nodule as FBNodule
import LungData.Dataset as FBDataset

from Utils import extract_nodules, outline_nodule, print_image

LIDC_XML_DIR = ""
DCM_FILE_MAP_JSON = ""
RAW_IMAGE_DIR = ""
PROCESSED_IMAGE_DIR = ""
BIN_DEST = ""



