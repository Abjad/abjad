from abjad.spanner.new import NewSpanner


class _Tempo(NewSpanner):

   def __init__(self, music):
      NewSpanner.__init__(self, music)
      self.tempo = None

   def _before(self, leaf):
      result = [ ]
      if self._isMyFirstLeaf(leaf):
         if self.tempo:
            result.append(r'\tempo %s=%s' % self.tempo)
      return result
