# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_OctaveTranspositionMapping__one_line_menuing_summary_01():

    mapping = pitchtools.OctaveTranspositionMapping(
        [('[A0, C4)', 15), ('[C4, C8)', 27)],
        )

    string = 'mapping: [A0, C4) => 15, [C4, C8) => 27'
    assert mapping._one_line_menuing_summary == string
