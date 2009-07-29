from abjad.tempo.proportional.format import _TempoProportionalFormatInterface
from abjad.tempo.spanner import Tempo
import types


class TempoProportional(Tempo):
   r'''.. versionadded:: 1.1.1

   Tempo spanner aware of score-global spacing. ::

      abjad> t = Score([Staff(construct.scale(4))])   
      abjad> tempo_indication = TempoIndication(Rational(1, 4), 60)   
      abjad> spacing_indication = SpacingIndication(tempo_indication, Rational(1, 34))   
      abjad> t.global_spacing = spacing_indication   

   ::

      abjad> print t.format
      \new Score <<
              \new Staff {
                      c'8
                      d'8
                      e'8
                      f'8
              }
      >>

   ::

      abjad> p = TempoProportional(t[0][:2])   
      abjad> p.indication = TempoIndication(Rational(1, 4), 60)   
   
   ::

      abjad> p = TempoProportional(t[0][2:])   
      abjad> p.indication = TempoIndication(Rational(1, 4), 120)

   ::

      abjad> print t.format
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

   def __init__(self, music = None, indication = None):
      '''Init ``TempoProportional`` as type of ``Tempo`` spanner.'''
      Tempo.__init__(self, music, indication)
      self._format = _TempoProportionalFormatInterface(self)
