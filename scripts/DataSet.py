# automatically generated by the FlatBuffers compiler, do not modify

# namespace: LungData

import flatbuffers

class DataSet(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsDataSet(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = DataSet()
        x.Init(buf, n + offset)
        return x

    # DataSet
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # DataSet
    def Data(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .LungImage import LungImage
            obj = LungImage()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # DataSet
    def DataLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def DataSetStart(builder): builder.StartObject(1)
def DataSetAddData(builder, data): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(data), 0)
def DataSetStartDataVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def DataSetEnd(builder): return builder.EndObject()
