# automatically generated by the FlatBuffers compiler, do not modify

# namespace: TrainingData

import flatbuffers

class Header(object):
    __slots__ = ['_tab']

    # Header
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Header
    def InputRows(self): return self._tab.Get(flatbuffers.number_types.Uint32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(0))
    # Header
    def InputCols(self): return self._tab.Get(flatbuffers.number_types.Uint32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(4))
    # Header
    def OutputRows(self): return self._tab.Get(flatbuffers.number_types.Uint32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(8))
    # Header
    def OutputCols(self): return self._tab.Get(flatbuffers.number_types.Uint32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(12))
    # Header
    def NumExamples(self): return self._tab.Get(flatbuffers.number_types.Uint32Flags, self._tab.Pos + flatbuffers.number_types.UOffsetTFlags.py_type(16))

def CreateHeader(builder, inputRows, inputCols, outputRows, outputCols, numExamples):
    builder.Prep(4, 20)
    builder.PrependUint32(numExamples)
    builder.PrependUint32(outputCols)
    builder.PrependUint32(outputRows)
    builder.PrependUint32(inputCols)
    builder.PrependUint32(inputRows)
    return builder.Offset()
