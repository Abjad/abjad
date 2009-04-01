from abjad.spanner.grobhandler import _GrobHandlerSpanner


class _PositionalGrobHandlerSpanner(_GrobHandlerSpanner):

   def __init__(self, grob, music = None):
      _GrobHandlerSpanner.__init__(self, grob, music)

   ## PRIVATE ATTRIBUTES ##

   def _before(self, leaf):
      result = [ ]
      result.extend(_GrobHandlerSpanner._before(self, leaf))
      if self._isMyFirstLeaf(leaf):
         if not self.position is None:
            result.append(self._positions[self.position])
      return result

   ## PUBLIC ATTRIBUTES ##

   @apply
   def position( ):
      def fget(self):
         return self._position
      def fset(self, arg):
         if not arg in self._positions.keys( ):
            raise ValueError(
               "Position must be one of %s" % self._positions.keys( ))
         self._position = arg
      return property(**locals( ))
