from abjad.spanner.grobhandler import _GrobHandlerSpanner


class Slur(_GrobHandlerSpanner):

   def __init__(self, music = None):
      _GrobHandlerSpanner.__init__(self, 'Slur', music)
      self.position = None

   ### PUBLIC ATTRIBUTES ###
   
   ## TODO: position and _before attributes are the same for this and other
   ## spanners such as TextSpanner. Should we have a shared parent class
   ## for these? An abstract _PositionalGrobHandlerSpanner that inherits
   ## from _GrobHandlerSpanner?

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
         
   ### PRIVATE ATTRIBUTES ###

   _positions = {'neutral':r'\slurNeutral', 'up':r'\slurUp', 
                 'down':r'\slurDown', None:None}

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
         result.append('(')
      if self._isMyLastLeaf(leaf):
         result.append(')')   
      return result
