# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.indicatortools import LilyPondComment


def test_indicatortools_LilyPondComment___repr___01():
    r'''Repr of unattached comment is evaluable.
    '''

    comment_1 = indicatortools.LilyPondComment('foo')
    comment_2 = eval(repr(comment_1))

    assert isinstance(comment_1, indicatortools.LilyPondComment)
    assert isinstance(comment_2, indicatortools.LilyPondComment)
    assert comment_1 == comment_2
