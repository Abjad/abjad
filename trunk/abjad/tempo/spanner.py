#from abjad.spanner.spanner import Spanner
from abjad.spanner.grobhandler import _GrobHandlerSpanner


### TODO - Implement a TempoIndication class to take pair
###        of (Rational, tempo).

#class _Tempo(Spanner):
class Tempo(_GrobHandlerSpanner):

   def __init__(self, music = None, tempo = None):
      #Spanner.__init__(self, music)
      _GrobHandlerSpanner.__init__(self, 'MetronomeMark', music)
      self.tempo = tempo

   ### PRIVATE METHODS ###

   ### TODO - Should we define an _after( ) method to indicate
   ###        where the effect of a tempo *ends*?

   def _before(self, leaf):
      result = [ ]
      result.extend(_GrobHandlerSpanner._before(self, leaf))
      if self._isMyFirstLeaf(leaf):
         if self.tempo:
            result.append(r'\tempo %s=%s' % self.tempo)
      return result

   ### PUBLIC ATTRIBUTES ###

   @apply
   def tempo( ):
      def fget(self):
         return self._tempo
      def fset(self, arg):
         self._tempo = arg 
      return property(**locals( ))
