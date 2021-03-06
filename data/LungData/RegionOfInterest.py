# automatically generated by the FlatBuffers compiler, do not modify

# namespace: LungData

import flatbuffers

class RegionOfInterest(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsRegionOfInterest(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = RegionOfInterest()
        x.Init(buf, n + offset)
        return x

    # RegionOfInterest
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # RegionOfInterest
    def ImageSOPUID(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return ""

    # RegionOfInterest
    def Inclusion(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos)
        return 0

    # RegionOfInterest
    def Contour(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 8
            from .Point import Point
            obj = Point()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # RegionOfInterest
    def ContourLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def RegionOfInterestStart(builder): builder.StartObject(3)
def RegionOfInterestAddImageSOPUID(builder, imageSOPUID): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(imageSOPUID), 0)
def RegionOfInterestAddInclusion(builder, inclusion): builder.PrependBoolSlot(1, inclusion, 0)
def RegionOfInterestAddContour(builder, contour): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(contour), 0)
def RegionOfInterestStartContourVector(builder, numElems): return builder.StartVector(8, numElems, 4)
def RegionOfInterestEnd(builder): return builder.EndObject()
