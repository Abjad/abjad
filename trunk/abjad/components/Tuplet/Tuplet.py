from abjad.components.Container import Container
from abjad.components.Tuplet._TupletDurationInterface import _TupletDurationInterface
from abjad.components.Tuplet._TupletFormatter import _TupletFormatter


class Tuplet(Container):
   r'''The Abjad model of a tuplet:

   ::

      abjad> tuplet = Tuplet((2, 3), macros.scale(3))
      abjad> f(tuplet)
      \times 2/3 {
         c'8
         d'8
         e'8
      }
   '''

   __slots__ = ('_force_fraction', '_is_invisible', '_signifier', )

   def __init__(self, multiplier, music = None, **kwargs):
      Container.__init__(self, music)
      self._duration = _TupletDurationInterface(self, multiplier)
      self._force_fraction = None
      self._formatter = _TupletFormatter(self) 
      self._is_invisible = None
      self._signifier = '*'
      self._initialize_keyword_values(**kwargs)

   ## OVERLOADS ##

   def __add__(self, arg):
      '''Add two tuplets of same type and with same multiplier.'''
      from abjad.tools import tuplettools
      assert isinstance(arg, type(self))
      new = tuplettools.fuse_tuplets([self, arg])
      return new
      
   def __repr__(self):
      return '%s(%s, [%s])' % (
         self.__class__.__name__, self.duration.multiplier, self._summary)

   def __str__(self):
      if 0 < len(self):
         return '{%s %s %s %s}' % (self._signifier, self.ratio, self._summary, self._signifier)
      else:
         return '{%s %s %s}' % (self._signifier, self.duration.multiplier, self._signifier)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _summary(self):
      if 0 < len(self):
         return ', '.join([str(x) for x in self._music])
      else:
         return ' '

   @property
   def _is_visible(self):
      return not self.is_invisible

   ## PUBLIC ATTRIBUTES ##

   @property
   def duration(self):
      '''Tuplet duration interface.'''
      return self._duration

   @apply
   def force_fraction( ):
      def fget(self):
         '''Read / write boolean to force ``n:m`` fraction.
         '''
         return self._force_fraction
      def fset(self, arg):
         if isinstance(arg, (bool, type(None))):
            self._force_fraction = arg
         else:
            raise TypeError('bad type for tuplet force fraction: "%s".' % arg)
      return property(**locals( ))

   @apply
   def is_invisible( ):
      def fget(self):
         '''Read / write boolean to render tuplet invisible.'''
         return self._is_invisible
      def fset(self, arg):
         assert isinstance(arg, (bool, type(None)))
         self._is_invisible = arg
      return property(**locals( ))

   @property
   def is_trivial(self):
      '''True when tuplet multiplier is one, otherwise False.'''
      return self.duration.multiplier == 1

   @property
   def ratio(self):
      '''Tuplet multiplier formatted with colon as ratio.'''
      multiplier = self.duration.multiplier
      if multiplier is not None:
         return '%s:%s' % (multiplier.denominator, multiplier.numerator)
      else:
         return None
