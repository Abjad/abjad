from abjad.spanner.spanner import Spanner


class Glissando(Spanner):

   def __init__(self, music = None):
      Spanner.__init__(self, music)

   def _right(self, leaf):
      result = [ ]
      if not self._isMyLastLeaf(leaf):
         result.append(r'\glissando')
      return result
