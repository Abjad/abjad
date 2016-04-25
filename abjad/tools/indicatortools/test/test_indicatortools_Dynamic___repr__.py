# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_Dynamic___repr___01():
    r'''Dynamic returns nonempty string repr.
    '''

    repr = Dynamic('f').__repr__()
    assert isinstance(repr, str) and 0 < len(repr)
