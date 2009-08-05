from abjad import *


def test_tools_spacing_get_global_01( ):
   '''Return ``global_spacing`` of effective score of ``component``.'''

   t = Score([Staff(construct.scale(4))])
   tempo_indication = TempoIndication(Rational(1, 8), 38)
   spacing_indication = SpacingIndication(tempo_indication, Rational(1, 68))
   t.global_spacing = spacing_indication

   r'''\new Score <<
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
           }
   >>'''

   assert spacing.get_global(t.leaves[0]) is spacing_indication
   assert spacing.get_global(t[0]) is spacing_indication
   assert spacing.get_global(t) is spacing_indication


def test_tools_spacing_get_global_02( ):
   '''Return ``None`` when effective score has no global spacing.'''

   t = Score([Staff(construct.scale(4))])

   r'''\new Score <<
           \new Staff {
                   c'8
                   d'8
                   e'8
                   f'8
           }
   >>'''

   assert spacing.get_global(t.leaves[0]) is None
   assert spacing.get_global(t[0]) is None
   assert spacing.get_global(t) is None


def test_tools_spacing_get_global_03( ):
   '''Return ``None`` when effective score is ``None``.'''

   t = Staff(construct.scale(4))

   assert spacing.get_global(t.leaves[0]) is None
   assert spacing.get_global(t[0]) is None
   assert spacing.get_global(t) is None
