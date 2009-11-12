from abjad.exceptions import UndefinedSpacingError
from abjad.exceptions import UndefinedTempoError
from abjad.rational import Rational
from abjad.spanners.spanner.grobhandler import _GrobHandlerSpanner
from abjad.spanners.tempo.format import _TempoSpannerFormatInterface
from abjad.tools import tempotools
import types


class TempoSpanner(_GrobHandlerSpanner):
   r'''Apply tempo indication to zero or more contiguous components.

   Handle LilyPond ``MetronomeMark`` grob.

   Handle LilyPond ``proportionalNotationDuration`` context setting.

   Invoke LilyPond ``\newSpacingSection`` command. ::

      abjad> t = Voice(construct.scale(4))
      abjad> tempo_indication = tempotools.TempoIndication(Rational(1, 8), 38)
      abjad> p = TempoSpanner(t[:], tempo_indication)
      abjad> f(t)
      \new Voice {
              \tempo 8=38
              c'8
              d'8
              e'8
              f'8
              %% tempo 8=38 ends here
      }
   '''

   def __init__(self, music = None, tempo_indication = None):
      _GrobHandlerSpanner.__init__(self, 'MetronomeMark', music)
      self._format = _TempoSpannerFormatInterface(self)
      self._proportional_notation_duration_effective = None
      self._proportional_notation_duration_reference = None
      self.tempo_indication = tempo_indication
      self.reference = None

   ## OVERRIDES ##

   def __repr__(self):
      name = self.__class__.__name__
      summary = self._compact_summary
      if self.tempo_indication is not None:
         equation = self.tempo_indication._equation
         return '%s(%s, %s)' % (name, equation, summary)
      else:
         return '%s(%s)' % (name, summary) 

   ## PUBLIC ATTRIBUTES ##

   @property
   def proportional_notation_duration_effective(self):
      '''Read-only LilyPond proportionalNotationDuration.
      Raises UndefinedTempoError if reference tempo undefined.
      Raises UndefinedSpacingError if reference spacing undefined.

      .. todo:: Write Tempo.proportional_notation_duration_effective( )
         tests.
      '''
      reference = self.proportional_notation_duration_reference
      if reference is not None:
         return self.scaling_factor * reference
      raise UndefinedSpacingError

   @apply
   def proportional_notation_duration_reference( ):
      def fget(self):
         '''Read / write LilyPond proportionalNotationDuration.
         Must be rational-valued duration.

         .. todo:: Write Tempo.proportional_notation_duration_reference( )
            tests.
         '''
         return self._proportional_notation_duration_reference
      def fset(self, arg):
         assert isinstance(arg, Rational)
         assert 0 < arg
         self._proportional_notation_duration_reference = arg
      return property(**locals( ))

   @apply
   def reference( ):
      def fget(self):
         '''Read / write reference tempo indication.
         If set, scale durations at format-time.'''
         return self._reference
      def fset(self, arg):
         assert isinstance(arg, (tempotools.TempoIndication, types.NoneType))
         self._reference = arg 
      return property(**locals( ))

   @property
   def scaling_factor(self):
      '''Reference tempo divided by indicated tempo.'''
      try:
         return self.reference.quarters_per_minute / self.tempo_indication.quarters_per_minute
      except AttributeError:
         raise UndefinedTempoError

   @apply
   def tempo_indication( ):
      def fget(self):
         '''Read / write tempo indication.'''
         return self._tempo_indication
      def fset(self, arg):
         assert isinstance(arg, (tempotools.TempoIndication, types.NoneType))
         if isinstance(arg, tempotools.TempoIndication):
            self._tempo_indication = tempotools.TempoIndication(arg)
         elif isinstance(arg, types.NoneType):
            self._tempo_indication = arg 
         else:
            raise ValueError('must be Abjad TempoIndication or None.')
      return property(**locals( ))
