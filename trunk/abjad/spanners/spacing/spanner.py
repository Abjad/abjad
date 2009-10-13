from abjad.rational import Rational
from abjad.spanner.grobhandler import _GrobHandlerSpanner
from abjad.spanners.spacing.format import _SpacingSpannerFormatInterface
import types


class SpacingSpanner(_GrobHandlerSpanner):
   r'''Model a spacing section of musical score.

   Interface to LilyPond ``\newSpacingSection`` command.
   
   Interface to LilyPond ``proportionalNotationDuration`` context setting.

   Handle LilyPond ``SpacingSpanner`` grob. ::

      abjad> staff = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
      abjad> pitchtools.diatonicize(staff)
      abjad> spacing_spanner = SpacingSpanner(staff[1:])
      abjad> spacing_spanner.new_section = True
      abjad> spacing_spanner.proportional_notation_duration = Rational(1, 30)
      abjad> spacing_spanner.strict_grace_spacing = True
      abjad> spacing_spanner.strict_note_spacing = True
      abjad> spacing_spanner.uniform_stretching = True
      abjad> overridetools.promote(spacing_spanner, 'strict_grace_spacing', 'Score')
      abjad> overridetools.promote(spacing_spanner, 'strict_note_spacing', 'Score')
      abjad> overridetools.promote(spacing_spanner, 'uniform_stretching', 'Score')

   ::

      abjad> print staff.format
      \new Staff {
              {
                      \time 2/8
                      c'8
                      d'8
              }
              {
                      \time 2/8
                      \newSpacingSection
                      \set Score.proportionalNotationDuration = #(ly:make-moment 1 30)
                      \override Score.SpacingSpanner #'strict-grace-spacing = ##t
                      \override Score.SpacingSpanner #'strict-note-spacing = ##t
                      \override Score.SpacingSpanner #'uniform-stretching = ##t
                      e'8
                      f'8
                      \revert Score.SpacingSpanner #'strict-note-spacing
                      \revert Score.SpacingSpanner #'strict-grace-spacing
                      \revert Score.SpacingSpanner #'uniform-stretching
                      %%% spacing section ends here %%%
              }
      }

   '''

   def __init__(self, music = None):
      r'''Handle LilyPond ``SpacingSpanner`` grob.
      Handle LilyPond ``\newSpacingSection`` command.
      Interface to LilyPond ``proportionalNotationDuration`` context
      property.
      Init ``new_section`` as ``None``.
      '''

      _GrobHandlerSpanner.__init__(self, 'SpacingSpanner', music)
      self._format = _SpacingSpannerFormatInterface(self)
      self.new_section = None
      self.proportional_notation_duration = None

   ## PUBLIC ATTRIBUTES ##

   @apply
   def new_section( ):
      def fget(self):
         r'''Read / write interface to LilyPond 
         ``\newSpacingSection`` command.

         Set to ``True``, ``False`` or ``None``. ::

            abjad> staff = Staff(construct.scale(4))
            abjad> spacing_spanner = SpacingSpanner(staff[:])
            abjad> spacing_spanner.new_section = True
            abjad> print staff.format
            \new Staff {
                    \newSpacingSection
                    c'8
                    d'8
                    e'8
                    f'8
                    %%% spacing section ends here %%%
            }
         '''
         return self._new_section
      def fset(self, expr):
         assert isinstance(expr, (bool, types.NoneType))
         self._new_section = expr
      return property(**locals( ))

   @apply
   def proportional_notation_duration( ):
      def fget(self):
         r'''Read / write interface to LilyPond
         ``proportionalNotationDuration`` context property.

         Set to a rational value or ``None``. ::

            abjad> staff = Staff(construct.scale(4))
            abjad> spacing_spanner = SpacingSpanner(staff[2:])
            abjad> spacing_spanner.new_section = True
            abjad> spacing_spanner.proportional_notation_duration = Rational(1, 30)
            abjad> print t.format
            \new Staff {
                    c'8
                    d'8
                    \newSpacingSection
                    \set Score.proportionalNotationDuration = #(ly:make-moment 1 30)
                    e'8
                    f'8
                    %%% spacing section ends here %%%
            }

         .. note:: For ``propportional_notation_duration`` settings to have 
            any effect, you must also create a new spacing section with 
            ``new_section = True``.
         '''
         return self._proportional_notation_duration
      def fset(self, expr):
         assert isinstance(expr, (Rational, types.NoneType))
         self._proportional_notation_duration = expr
      return property(**locals( ))
