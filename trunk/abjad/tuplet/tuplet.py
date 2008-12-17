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

   ### REPR ###

   @property
   def _summary(self):
      if len(self) > 0:
         return ', '.join([str(x) for x in self._music])
      else:
         return ' '

   def __repr__(self):
      if len(self) > 0:
         return '_Tuplet(%s)' % self._summary
      else:
         return '_Tuplet( )'

   ### PROPERTIES ###

   ### TODO - replace either with managed attribute OR
   ###        even better, a TupletNumber grob for
   ###        LilyPond \override TupletNumber #'fraction = True
   ###        type of dynamic overrides.

   @property
   def ratio(self):
      if self.duration.multiplier:
         return _Ratio(*(~self.duration.multiplier).pair)
      else:
         return None

   ### MANAGED ATTRIBUTES ###

   @apply
   def invisible( ):
      def fget(self):
         return self._invisible
      def fset(self, arg):
         assert isinstance(arg, bool)
         self._invisible = arg
      return property(**locals())
