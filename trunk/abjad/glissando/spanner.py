from abjad.spanner.spanner import _Spanner


class Glissando(_Spanner):

   def __init__(self, music):
      _Spanner.__init__(self, music)

   def _right(self, leaf):
      result = [ ]
      if not self._isMyLastLeaf(leaf):
         result.append(r'\glissando')
      return result
