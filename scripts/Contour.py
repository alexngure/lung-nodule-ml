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
    def Points(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 8
            from .Point import Point
            obj = Point()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # Contour
    def PointsLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def ContourStart(builder): builder.StartObject(1)
def ContourAddPoints(builder, points): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(points), 0)
def ContourStartPointsVector(builder, numElems): return builder.StartVector(8, numElems, 4)
def ContourEnd(builder): return builder.EndObject()
