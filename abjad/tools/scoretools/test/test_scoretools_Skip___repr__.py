# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.scoretools import Skip


def test_scoretools_Skip___repr___01():
    r'''Skip repr is evaluable.
    '''

    skip_1 = Skip('s8.')
    skip_2 = eval(repr(skip_1))

    assert isinstance(skip_1, Skip)
    assert isinstance(skip_2, Skip)
    assert format(skip_1) == format(skip_2)
    assert skip_1 is not skip_2
