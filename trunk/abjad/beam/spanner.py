from abjad.spanner.spanner import Spanner


class Beam(Spanner):

   def __init__(self, music):
      Spanner.__init__(self, music)

   def _right(self, leaf):
      result = [ ]
      if self._isMyFirstLeaf(leaf):
         result.append('[')
      if self._isMyLastLeaf(leaf):
         result.append(']')   
      return result
