# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_Clef___repr___01():
    r'''Clef returns a nonempty repr string.
    '''

    repr = Clef('treble').__repr__()
    assert isinstance(repr, str) and 0 < len(repr)
