from abjad.spanner.new import NewSpanner


class Glissando(NewSpanner):

   def __init__(self, music):
      NewSpanner.__init__(self, music)

   def _right(self, leaf):
      result = [ ]
      if not self._isMyLastLeaf(leaf):
         result.append(r'\glissando')
      return result
