from abjad.component.component import _Component


def get_scorewide(component):
   '''Return scorewide spacing of explicit score of `compoment`. ::

      abjad> score = Score([Staff(construct.scale(4))])
      abjad> tempo_indication = tempotools.TempoIndication(Rational(1, 8), 44)
      abjad> spacing_indication = spacing.SpacingIndication(tempo_indication, Rational(1, 68))
      abjad> score.spacing.scorewide = spacing_indication 
      abjad> spacing.get_scorewide(score.leaves[0])
      SpacingIndication(TempoIndication(8, 44), 1/68)

   If no explicit score, return none. ::

      abjad> note = Note(0, (1, 4))
      abjad> spacing.get_scorewide(note) is None
      True
   
   .. versionchanged:: 1.1.2
      Name changed from ``spacing.get_global()`` to ``spacing.get_scorewide()``.
   '''

   if not isinstance(component, _Component):
      raise TypeError('must be Abjad component.')

   explicit_score = component.score.explicit
   if explicit_score is not None:
      return explicit_score.spacing.scorewide
