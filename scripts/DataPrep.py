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

def create_FBNodule(builder,my_nodule):
    """Takes an instance of the non-flatbuffers implementation of the Nodule class and
    converts it into a buffer.
    """
    ROI_list = []
    for item in my_nodule.ROI_list():
        ROI_list.append(create_FBROI(builder,item))
    FBNodule.NoduleStartROIVector(builder,len(ROI_list))
    for roi in ROI_list:
        builder.PrependUOffsetTRelative(roi)
    ROI_vec = builder.EndVector(len(ROI_list))
    nodule_ID = builder.CreateString(my_nodule.noduleID())
    FBNodule.NoduleStart(builder)
    FBNodule.NoduleAddNoduleId(builder,nodule_ID)
    characteristics = my_nodule.characteristics()
    if characteristics is not None:
        FBNodule.NoduleAddSubtlety(builder,characteristics._subtlety)
        FBNodule.NoduleAddInternalStructure(builder,characteristics._internal_structure)
        FBNodule.NoduleAddCalcification(builder,characteristics._calcification)
        FBNodule.NoduleAddSphericity(builder,characteristics._sphericity)
        FBNodule.NoduleAddMargin(builder,characteristics._margin)
        FBNodule.NoduleAddLobulation(builder,characteristics._lobulation)
        FBNodule.NoduleAddSpiculation(builder,characteristics._spiculation)
        FBNodule.NoduleAddTexture(builder,characteristics._texture)
        FBNodule.NoduleAddMalignancy(builder,characteristics._malignancy)
    FBNodule.NoduleAddROI(builder,ROI_vec)
    nodule = FBNodule.NoduleEnd(builder)
    return nodule


