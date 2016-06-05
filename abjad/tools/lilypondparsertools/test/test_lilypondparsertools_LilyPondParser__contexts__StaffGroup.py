# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__contexts__StaffGroup_01():

    target = scoretools.StaffGroup([])

    assert format(target) == stringtools.normalize(
        r'''
        \new StaffGroup <<
        >>
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
