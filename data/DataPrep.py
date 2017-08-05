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

nodule_map = {}

def create_FBROI(builder,my_ROI):
    """Takes an instance of the non-flatbuffers implementation of the ROI class and
    converts it into a buffer.
    """
    UID_str = my_ROI.image_UID()
    roi_coords = my_ROI.contour()
    if UID_str not in nodule_map:
        nodule_map[UID_str] = {}
        nodule_map[UID_str]['roi_count']  = 0
    else:
        nodule_map[UID_str]['roi_count'] += 1
    roi_count = nodule_map[UID_str]['roi_count']
    roi_uid = 'roi_'+str(roi_count)

    contour_lst = []
    FBROI.RegionOfInterestStartContourVector(builder,len(roi_coords))
    for coord in my_ROI.contour():
        builder.PrependUOffsetTRelative(FBPoint.CreatePoint(builder,coord[0],coord[1]))
        contour_lst.append([coord[0],coord[1]])
    nodule_map[UID_str][roi_uid] = contour_lst
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

def create_dataset_buffer(lidc_xml):
    """Takes a list of LIDC xml files and creates a flatbuffers Dataset
    object.
    """
    builder = flatbuffers.Builder(0)
    nodule_list = []
    for xml_file in lidc_xml:
        nodule_list.extend(extract_nodules(xml_file))
    nodule_vec = []
    for item in nodule_list:
        nodule_vec.append(create_FBNodule(builder,item))
    FBDataset.DatasetStartDataVector(builder,len(nodule_vec))
    for nodule in nodule_vec:
        builder.PrependUOffsetTRelative(nodule)
    data = builder.EndVector(len(nodule_list))
    FBDataset.DatasetStart(builder)
    FBDataset.DatasetAddData(builder,data)
    dataset = FBDataset.DatasetEnd(builder)
    builder.Finish(dataset)
    return builder.Bytes,builder.head

def main():
    """Create a Dataset object and output the resulting buffer as a binary
    file.
    """
    lidc_xml_dir = r"lidc-xml/188"
    xml_files = []
    for file in os.listdir(lidc_xml_dir):
        xml_files.append(os.path.join(lidc_xml_dir,file))

    databuffer,head=create_dataset_buffer(xml_files)

    bin_dest = "lidc-xml/lidc.lng"
    json_dest = 'lidc-xml/nodule_map.json'
    with open(bin_dest,'wb') as bin_file:
        bin_file.write(databuffer[head:])

    with open(json_dest,'w') as json_file:
        json.dump(nodule_map,json_file,indent=4)

if __name__ == '__main__':
    main()
