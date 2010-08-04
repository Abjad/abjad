from abjad.interfaces.SpacingInterface.SpacingInterface import SpacingInterface
from abjad.core import Rational
from abjad.tools.spacingtools.SpacingIndication import SpacingIndication
import types


class ScoreSpacingInterface(SpacingInterface):
   r'''Handle LilyPond ``SpacingSpanner`` grob.

   Receive Abjad ``SpacingSpanner``.

   Interface to LilyPond ``proportionalNotationDuration`` context
   property.

   Special read / write `scorewide` spacing attribute to manage
   scorewide spacing.

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
      SpacingInterface.__init__(self, _client)
      self.scorewide = None

   ## PUBLIC ATTRIBUTES ##

   @apply
   def scorewide( ):
      def fget(self):
         '''Special read / write attribute to manage score-global spacing.

         Assign Abjad :class:`~abjad.spacing.SpacingIndication` or ``None``.

         Set to activate Abjad :class:`~abjad.TempoProportional` spanners.
         '''
         return self._scorewide
      def fset(self, expr):
         assert isinstance(expr, (SpacingIndication, types.NoneType))
         self._scorewide = expr
      return property(**locals( ))
