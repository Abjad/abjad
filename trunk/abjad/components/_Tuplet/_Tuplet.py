from abjad.components.Container import Container
from abjad.components._Tuplet._TupletDurationInterface import _TupletDurationInterface
from abjad.components._Tuplet._TupletFormatter import _TupletFormatter
import types


class _Tuplet(Container):
   '''Abjad tuplet formalization.
   '''

   def __init__(self, music = None):
      '''Init tuplet as type of Abjad container.'''
      Container.__init__(self, music)
      self._duration = _TupletDurationInterface(self)
      self._force_fraction = None
      self._formatter = _TupletFormatter(self) 
      self._invisible = False

   ## OVERLOADS ##

   def __add__(self, arg):
      '''Add two tuplets of same type and with same multiplier.'''
      from abjad.tools import tuplettools
      assert isinstance(arg, type(self))
      new = tuplettools.fuse_tuplets([self, arg])
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

   @property
   def _visible(self):
      return not self.invisible

   ## PUBLIC ATTRIBUTES ##

   @apply
   def force_fraction( ):
      '''Read / write boolean to force n:m fraction.'''
      def fget(self):
         return self._force_fraction
      def fset(self, arg):
         if isinstance(arg, (bool, types.NoneType)):
            self._force_fraction = arg
         else:
            raise TypeError
      return property(**locals( ))

   @apply
   def invisible( ):
      def fget(self):
         '''Read / write boolean to render tuplet invisible.'''
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
