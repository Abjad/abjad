from abjad.container.container import Container
from abjad.tuplet.duration import _TupletDurationInterface
from abjad.tuplet.formatter import _TupletFormatter
from abjad.tuplet.ratio import _Ratio


class _Tuplet(Container):

   def __init__(self, music = None):
      music = music or [ ]
      Container.__init__(self, music)
      self.brackets = 'curly'
      self._duration = _TupletDurationInterface(self)
      self.formatter = _TupletFormatter(self) 
      self._invisible = False

   ### OVERLOADS ###

   def __repr__(self):
      if len(self) > 0:
         return '_Tuplet(%s)' % self._summary
      else:
         return '_Tuplet( )'

   ### PRIVATE ATTRIBUTES ###

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

   ## TODO - replace either with managed attribute OR
   ##        even better, a TupletNumber grob for
   ##        LilyPond \override TupletNumber #'fraction = True
   ##        type of dynamic overrides.

   @property
   def ratio(self):
      '''Read-only reference to tuplet ratio as a Rational.'''
      if self.duration.multiplier:
         return _Ratio(self.duration.multiplier)
      else:
         return None

   @property
   def trivial(self):
      '''True when tuplet ratio is one, otherwise False.'''
      return self.ratio == 1
