from abjad.container.container import Container
from abjad.tuplet.duration import _TupletDurationInterface
from abjad.tuplet.formatter import _TupletFormatter


class _Tuplet(Container):
   '''*Abjad* model of musical tuplet.'''

   def __init__(self, music = None):
      '''Init tuplet as type of *Abjad* container.'''
      Container.__init__(self, music)
      self._duration = _TupletDurationInterface(self)
      self._formatter = _TupletFormatter(self) 
      self._invisible = False

   ## OVERLOADS ##

   def __add__(self, arg):
      '''Add two tuplets of same type and with same multiplier.'''
      from abjad.tools import fuse
      assert isinstance(arg, type(self))
      new = fuse.tuplets_by_reference([self, arg])
      return new
      
   def __repr__(self):
      if len(self) > 0:
         return '_Tuplet(%s)' % self._summary
      else:
         return '_Tuplet( )'

   ## PRIVATE ATTRIBUTES ##

   @property
   def _summary(self):
      if len(self) > 0:
         return ', '.join([str(x) for x in self._music])
      else:
         return ' '

   ## PUBLIC ATTRIBUTES ##

   @apply
   def invisible( ):
      '''Read / write boolean to render tuplet invisible.'''
      def fget(self):
         return self._invisible
      def fset(self, arg):
         assert isinstance(arg, bool)
         self._invisible = arg
      return property(**locals())

   @property
   def ratio(self):
      '''Tuplet multiplier formatted with colon as ratio.'''
      multiplier = self.duration.multiplier
      if multiplier is not None:
         return '%s:%s' % (multiplier._d, multiplier._n)
      else:
         return None

   @property
   def trivial(self):
      '''True when tuplet multiplier is one, otherwise False.'''
      return self.duration.multiplier == 1
