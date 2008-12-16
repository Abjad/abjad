from abjad.core.spanner import _Spanner


class Beam(_Spanner):

   def __init__(self, music):
      _Spanner.__init__(self, music)

   def _right(self, leaf):
      result = [ ]
      if self._isMyFirstLeaf(leaf):
         result.append('[')
      if self._isMyLastLeaf(leaf):
         result.append(']')   
      return result
