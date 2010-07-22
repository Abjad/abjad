from abjad import *


def test_SpacingIndication_normalized_spacing_duration_01( ):
   '''LilyPond proportionalNotationDuration setting required 
   for this spacing indication at quarter equals 60.'''

   tempo_indication = tempotools.TempoIndication(Rational(1, 4), 120)
   spacing_indication = spacingtools.SpacingIndication(tempo_indication, Rational(1, 16))
   assert spacing_indication.normalized_spacing_duration == Rational(1, 32)


def test_SpacingIndication_normalized_spacing_duration_02( ):
   '''LilyPond proportionalNotationDuration setting required
   for this spacing indication at quarter equals 60
   is the same as the proportional notation duration set
   on this spacing indication when tempo indication set
   on this spacing indication is already quarter equals 60.'''

   tempo_indication = tempotools.TempoIndication(Rational(1, 4), 60)
   spacing_indication = spacingtools.SpacingIndication(tempo_indication, Rational(1, 68))
   assert spacing_indication.normalized_spacing_duration == Rational(1, 68)
