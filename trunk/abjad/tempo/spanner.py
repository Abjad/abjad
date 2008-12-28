#from abjad.spanner.spanner import Spanner
from abjad.spanner.grobhandler import _GrobHandlerSpanner


#class _Tempo(Spanner):
class _Tempo(_GrobHandlerSpanner):

   def __init__(self, music = None):
      #Spanner.__init__(self, music)
      _GrobHandlerSpanner.__init__(self, 'MetronomeMark', music)
      self.tempo = None

   def _before(self, leaf):
      result = [ ]
      result.extend(_GrobHandlerSpanner._before(leaf))
      if self._isMyFirstLeaf(leaf):
         if self.tempo:
            result.append(r'\tempo %s=%s' % self.tempo)
      return result
