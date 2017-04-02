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

def create_FBROI(builder,my_ROI):
    """Takes an instance of the non-flatbuffers implementation of the ROI class and
    converts it into a buffer.
    """
    roi_coords = my_ROI.contour()
    FBROI.RegionOfInterestStartContourVector(builder,len(roi_coords))
    for coord in my_ROI.contour():
        builder.PrependUOffsetTRelative(FBPoint.CreatePoint(builder,coord[0],coord[1]))
    contour = builder.EndVector(len(roi_coords))
    imageUID = builder.CreateString(my_ROI.image_UID())
    FBROI.RegionOfInterestStart(builder)
    FBROI.RegionOfInterestAddImageSOPUID(builder, imageUID)
    FBROI.RegionOfInterestAddInclusion(builder,my_ROI.inclusion())
    FBROI.RegionOfInterestAddContour(builder,contour)
    ROI = FBROI.RegionOfInterestEnd(builder)
    return ROI



