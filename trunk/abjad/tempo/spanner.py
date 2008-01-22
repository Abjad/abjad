from .. duration.duration import Duration
from .. core.spanner import _Spanner

class Tempo(_Spanner):

   def __init__(self, music):
      _Spanner.__init__(self, music)
      self.tempo = None

   def _before(self, leaf):
      result = [ ]
      if self._isMyFirstLeaf(leaf):
         if self.tempo:
            result.append(r'\tempo %s=%s' % self.tempo)
      return result
