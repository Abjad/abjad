# -*- coding: utf-8 -*-
from abjad import *


def test_selectiontools_VerticalMoment___repr___01():
    r'''Vertical moment repr returns a nonempty string.
    '''

    vertical_moment = inspect_(Note('c4')).get_vertical_moment()
    representation = repr(vertical_moment)

    assert isinstance(representation, str) and 0 < len(representation)
