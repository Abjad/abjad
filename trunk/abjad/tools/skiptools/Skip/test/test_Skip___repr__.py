# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.skiptools import Skip


def test_Skip___repr___01():
    r'''Skip repr is evaluable.
    '''

    skip_1 = Skip('s8.')
    skip_2 = eval(repr(skip_1))

    assert isinstance(skip_1, Skip)
    assert isinstance(skip_2, Skip)
    assert skip_1.lilypond_format == skip_2.lilypond_format
    assert skip_1 is not skip_2
