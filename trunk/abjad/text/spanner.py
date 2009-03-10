from abjad.spanner.grobhandler import _GrobHandlerSpanner


class Text(_GrobHandlerSpanner):

   def __init__(self, music = None):
      _GrobHandlerSpanner.__init__(self, 'TextSpanner', music)
      self.position = None

   ## PRIVATE ATTRIBUTES ##

   _positions = {'neutral':r'\textSpannerNeutral', 
      'up':r'\textSpannerUp', 'down':r'\textSpannerDown', None:None}

   ## PRIVATE METHODS ##

   def _before(self, leaf):
      result = [ ]
      result.extend(_GrobHandlerSpanner._before(self, leaf))
      if self._isMyFirstLeaf(leaf):
         if not self.position is None:
            result.append(self._positions[self.position])
      return result

   def _right(self, leaf):
      result = [ ]
      if self._isMyFirstLeaf(leaf):
         result.append(r'\startTextSpan')
      if self._isMyLastLeaf(leaf):
         result.append(r'\stopTextSpan')   
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
