from abjad.spanners.TempoSpanner.TempoSpannerProportional.format import \
   _TempoProportionalFormatInterface
from abjad.spanners.TempoSpanner.TempoSpanner import TempoSpanner
import types


class TempoSpannerProportional(TempoSpanner):
   r'''.. versionadded:: 1.1.1

   Tempo spanner aware of scorewide spacing. ::

      abjad> score = Score([Staff(macros.scale(4))])   
      abjad> tempo_indication = tempotools.TempoIndication(Rational(1, 4), 60)   
      abjad> spacing_indication = spacing.SpacingIndication(tempo_indication, Rational(1, 34))   
      abjad> score.spacing.scorewide = spacing_indication   

   ::

      abjad> f(score)
      \new Score <<
              \new Staff {
                      c'8
                      d'8
                      e'8
                      f'8
              }
      >>

   ::

      abjad> tempo_indication = tempotools.TempoIndication(Rational(1, 4), 60)   
      abjad> proportional_tempo_spanner = TempoSpannerProportional(t[0][:2], tempo_indication)   
   
   ::

      abjad> tempo_indication = tempotools.TempoIndication(Rational(1, 4), 120)
      abjad> proportional_tempo_spanner = TempoSpannerProportional(t[0][2:], tempo_indication)   

   ::

      abjad> f(score)
      \new Score <<
              \new Staff {
                      \tempo 4=60
                      \newSpacingSection
                      \set Score.proportionalNotationDuration = #(ly:make-moment 1 34)
                      c'8
                      d'8
                      %% tempo 4=60 ends here
                      \tempo 4=120
                      \newSpacingSection
                      \set Score.proportionalNotationDuration = #(ly:make-moment 1 17)
                      e'8
                      f'8
                      %% tempo 4=120 ends here
              }
      >>
   '''

   def __init__(self, music = None, tempo_indication = None):
      TempoSpanner.__init__(self, music, tempo_indication)
      self._format = _TempoProportionalFormatInterface(self)
