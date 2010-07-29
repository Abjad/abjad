from abjad import *


def test_spacingtools_get_scorewide_spacing_01( ):
   '''Return global_spacing of effective score of component.'''

   t = Score([Staff(macros.scale(4))])
   tempo_indication = tempotools.TempoIndication(Rational(1, 8), 38)
   spacing_indication = spacingtools.SpacingIndication(
      tempo_indication, Rational(1, 68))
   t.spacing.scorewide = spacing_indication

   r'''
   \new Score <<
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
           }
   >>
   '''

   assert spacingtools.get_scorewide_spacing(t.leaves[0]) is spacing_indication
   assert spacingtools.get_scorewide_spacing(t[0]) is spacing_indication
   assert spacingtools.get_scorewide_spacing(t) is spacing_indication


def test_spacingtools_get_scorewide_spacing_02( ):
   '''Return None when effective score has no global spacing.'''

   t = Score([Staff(macros.scale(4))])

   r'''
   \new Score <<
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
           }
   >>
   '''

   assert spacingtools.get_scorewide_spacing(t.leaves[0]) is None
   assert spacingtools.get_scorewide_spacing(t[0]) is None
   assert spacingtools.get_scorewide_spacing(t) is None


def test_spacingtools_get_scorewide_spacing_03( ):
   '''Return None when effective score is None.'''

   t = Staff(macros.scale(4))

   assert spacingtools.get_scorewide_spacing(t.leaves[0]) is None
   assert spacingtools.get_scorewide_spacing(t[0]) is None
   assert spacingtools.get_scorewide_spacing(t) is None
