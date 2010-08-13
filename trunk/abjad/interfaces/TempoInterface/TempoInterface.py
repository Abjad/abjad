from abjad.core import _BacktrackingInterface
from abjad.core import _GrobHandler
from abjad.core import _Observer
from abjad.interfaces._SpannerReceptor import _SpannerReceptor
from abjad.core import Rational
from abjad.spanners import TempoSpanner
from abjad.tools import tempotools
import types


## TODO: Rename MetronomeMarkInterface ##

class TempoInterface(_Observer, _GrobHandler, 
   _BacktrackingInterface, _SpannerReceptor):
   '''Handle LilyPond MetronomeMark grob and Abjad TempoSpanner.

   The implementation of `effective` given here allows for
   tempo indication to be set either be a tempo spanner or
   by a forced value set directly on the tempo interface.
   As such, `TempoInterface` implements two different and
   competing patterns for the way in which tempo indications
   can be set.

   This probably isn't the best situation and, in fact, the
   implementation will clean up considerably is we allow for
   only one way to set tempo indications, most likely
   through spanners only.

   Both patterns remain for now, though this situation is
   unstable and should probably resolve at some point in 
   the future.
   '''
   
   def __init__(self, _client, _updateInterface):
      '''Bind to client and LilyPond MetronomMark grob.
         Receive Abjad TempoSpanner.'''
      _Observer.__init__(self, _client, _updateInterface)
      _GrobHandler.__init__(self, 'MetronomeMark')
      _BacktrackingInterface.__init__(self, 'tempo')
      _SpannerReceptor.__init__(self, (TempoSpanner, ))
      self._acceptableTypes = (tempotools.TempoIndication, )
      self._effective = None
      self._forced = None
      self._tempo_wholes_per_minute = None
 
   ## PRIVATE ATTRIBUTES ##

   @property
   def _opening(self):
      '''Format contribution at container opening or before leaf.'''
      result =  [ ] 
      if self.forced or self.change and not (
         self.spanned and self.spanner._is_my_first_leaf(self._client)):
         result.append(self.effective.format)
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def effective(self):
      '''Effective tempo governing client.
         Decisions here arbitrate between spanner and forced attribute.'''
      if self.forced:
         return self.forced
      if self.parented:
         return self.spanner_in_parentage.tempo_indication
      return _BacktrackingInterface.effective.fget(self)

   @property
   def settings(self):
      '''Read-only list of LilyPond context settings
      picked up at format-time.'''
      from abjad.components._Context import _Context
      result = [ ]
      tempo_wholes_per_minute = self.tempo_wholes_per_minute
      if tempo_wholes_per_minute is not None:
         numerator = tempo_wholes_per_minute.numerator
         denominator = tempo_wholes_per_minute.denominator
         if isinstance(self._client, _Context):
            setting = 'tempoWholesPerMinute = '
         else:
            setting = r'\set Score.tempoWholesPerMinute = '
         setting += '#(ly:make-moment %s %s)' % (numerator, denominator)
         result.append(setting)
      return result

   @apply
   def tempo_wholes_per_minute( ):
      def fget(self):
         '''Read / write LilyPond tempoWholesPerMinute conext setting.
         '''
         return self._tempo_wholes_per_minute
      def fset(self, expr):
         if expr is None:
            self._tempo_wholes_per_minute = expr
         else:
            rational = Rational(expr)
            self._tempo_wholes_per_minute = rational
      return property(**locals( ))
