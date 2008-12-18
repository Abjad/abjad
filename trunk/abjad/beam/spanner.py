from abjad.spanner.new import NewSpanner


class Beam(NewSpanner):

   def __init__(self, music):
      NewSpanner.__init__(self, music)

   def _right(self, leaf):
      result = [ ]
      if self._isMyFirstLeaf(leaf):
         result.append('[')
      if self._isMyLastLeaf(leaf):
         result.append(']')   
      return result
