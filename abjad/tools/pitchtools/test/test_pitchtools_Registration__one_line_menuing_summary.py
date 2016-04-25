# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Registration__one_line_menuing_summary_01():

    mapping = pitchtools.Registration(
        [('[A0, C4)', 15), ('[C4, C8)', 27)],
        )

    string = 'registration: [A0, C4) => 15, [C4, C8) => 27'
    assert mapping._one_line_menu_summary == string
