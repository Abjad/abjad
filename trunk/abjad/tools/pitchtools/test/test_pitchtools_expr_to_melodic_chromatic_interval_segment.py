from abjad import *


def test_pitchtools_expr_to_melodic_chromatic_interval_segment_01():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
    mciseg = pitchtools.expr_to_melodic_chromatic_interval_segment(staff)

    assert mciseg.melodic_chromatic_interval_numbers == (2, 2, 1, 2, 2, 2, 1)
