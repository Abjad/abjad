from abjad.core import _FormatContributor
from abjad.interfaces._Interface import _Interface
from abjad.interfaces._SpannerReceptor import _SpannerReceptor
from abjad.core import Rational
from abjad.spanners import SpacingSpanner
import types


class SpacingInterface(_Interface, _FormatContributor, _SpannerReceptor):
   r'''Handle LilyPond ``SpacingSpanner`` grob.

   Receive Abjad ``SpacingSpanner``.

   Interface to LilyPond ``proportionalNotationDuration`` context
   property.

   Example::

      abjad> t = Score([ ])
      abjad> t.spacing.proportional_notation_duration = Rational(1, 56)
      abjad> t.spacing.strict_grace_spacing = True
      abjad> t.spacing.strict_note_spacing = True
      abjad> t.spacing.uniform_stretching = True
      abjad> print t.format
      \new Score \with {
              \override SpacingSpanner #'strict-note-spacing = ##t
              \override SpacingSpanner #'uniform-stretching = ##t
              \override SpacingSpanner #'strict-grace-spacing = ##t
              \set proportionalNotationDuration = #(ly:make-moment 1 56)
      } <<
      >>
   
   LilyPond ``SpacingSpanner`` lives in score context by default.
   '''

   def __init__(self, _client):
      '''Bind to client. Handle LilyPond ``SpacingSpanner`` grob.
         Receive Abjad ``SpacingSpanner`` spanner.'''
      _Interface.__init__(self, _client)
      _FormatContributor.__init__(self)
      _SpannerReceptor.__init__(self, (SpacingSpanner, ))
      self.proportional_notation_duration = None

   ## PRIVATE ATTRIBUTES ##

   @property
   def _overrides(self):
      '''Read-only list of with-block context overrides.'''
      result = [ ]
      #result.extend(_GrobHandler._overrides.fget(self))
      pnd = self.proportional_notation_duration
      if pnd is not None:
         setting = r'proportionalNotationDuration = ' + \
            '#(ly:make-moment %s %s)' % (
            pnd._numerator, pnd._denominator)
         result.append(setting)
      return result

   ## PUBLIC ATTRIBUTES ##

   @apply
   def proportional_notation_duration( ):
      def fget(self):
         r'''Read / write interface to LilyPond
         ``proportionalNotationDuration`` context property.

         Set to a rational value or ``None``.

         .. todo:: Will only work on Abjad score. We need a general
            idea of 'settings promotion', similar to 'override promotion',
            if we want this to work with containers other than the Abjad score.

         ::

            abjad> t = Score([Staff(macros.scale(4))])
            abjad> t.spacing.proportional_notation_duration = Rational(1, 56)
            abjad> print t.format
            \new Score \with {
                    proportionalNotationDuration = #(ly:make-moment 1 56)
            } <<
                    \new Staff {
                            c'8
                            d'8
                            e'8
                            f'8
                    }
            >>
         '''
         return self._proportional_notation_duration
      def fset(self, expr):
         assert isinstance(expr, (Rational, type(None)))
         self._proportional_notation_duration = expr
      return property(**locals( ))
