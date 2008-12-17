from abjad.spanner.spanner import Spanner


class _Tempo(Spanner):

   def __init__(self, music):
      _Spanner.__init__(self, music)
      self.tempo = None

   def _before(self, leaf):
      result = [ ]
      if self._isMyFirstLeaf(leaf):
         if self.tempo:
            result.append(r'\tempo %s=%s' % self.tempo)
      return result
