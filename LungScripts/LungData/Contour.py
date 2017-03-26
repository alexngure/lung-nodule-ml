# automatically generated by the FlatBuffers compiler, do not modify

# namespace: LungData

import flatbuffers

class Contour(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsContour(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Contour()
        x.Init(buf, n + offset)
        return x

    # Contour
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Contour
    def ImageSOPUID(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.String(o + self._tab.Pos)
        return ""

    # Contour
    def Inclusion(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos)
        return 0

    # Contour
    def Outline(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 8
            from .Point import Point
            obj = Point()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Contour
    def OutlineLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(8))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def ContourStart(builder): builder.StartObject(3)
def ContourAddImageSOPUID(builder, imageSOPUID): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(imageSOPUID), 0)
def ContourAddInclusion(builder, inclusion): builder.PrependBoolSlot(1, inclusion, 0)
def ContourAddOutline(builder, outline): builder.PrependUOffsetTRelativeSlot(2, flatbuffers.number_types.UOffsetTFlags.py_type(outline), 0)
def ContourStartOutlineVector(builder, numElems): return builder.StartVector(8, numElems, 4)
def ContourEnd(builder): return builder.EndObject()
