from abjad import *


def test_OctaveTranspositionMapping__one_line_menuing_summary_01():

    mapping = pitchtools.OctaveTranspositionMapping(
        [('[A0, C4)', 15), ('[C4, C8)', 27)],
        name='middle register mapping')

    assert mapping._one_line_menuing_summary == \
        'middle register mapping: [A0, C4) => 15, [C4, C8) => 27'
