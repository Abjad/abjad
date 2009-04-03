from abjad.pitch.pitch import Pitch
from abjad.spanner.grobhandler import _GrobHandlerSpanner


class Trill(_GrobHandlerSpanner):

   def __init__(self, music = None):
      _GrobHandlerSpanner.__init__(self, 'TrillSpanner', music)
      self._pitch = None

   ## PUBLIC ATTRIBUTES ##

   @apply
   def pitch( ):
      def fget(self):
         return self._pitch
      def fset(self, expr):
         if expr == None:
            self._pitch = None
         elif isinstance(expr, (int, float, long)):
            self._pitch = Pitch(expr)
         elif isinstance(expr, Pitch):
            self._pitch = Pitch
         else:
            raise ValueError('can not set trill pitch.')
      return property(**locals( ))

   ## PUBLIC METHODS ##

   def left(self, leaf):
      result = [ ]
      if self.pitch is not None:
         if self._isMyFirstLeaf(leaf):
            result.append(r'\pitchedTrill')
      return result

   def right(self, leaf):
      result = [ ]
      if self._isMyFirstLeaf(leaf):
         result.append(r'\startTrillSpan')
         if self.pitch is not None:
            result.append(str(self.pitch))
      if self._isMyLastLeaf(leaf):
         result.append(r'\stopTrillSpan')
      return result
