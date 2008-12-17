from abjad.pitch.pitch import Pitch
from abjad.spanner.spanner import _Spanner


class Trill(_Spanner):

   def __init__(self, music):
      _Spanner.__init__(self, music)
      self._pitch = None

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

   def _left(self, leaf):
      result = [ ]
      if self.pitch is not None:
         if self._isMyFirstLeaf(leaf):
            result.append(r'\pitchedTrill')
      return result

   def _right(self, leaf):
      result = [ ]
      if self._isMyFirstLeaf(leaf):
         result.append(r'\startTrillSpan')
         if self.pitch is not None:
            result.append(str(self.pitch))
      if self._isMyLastLeaf(leaf):
         result.append(r'\stopTrillSpan')
      return result
