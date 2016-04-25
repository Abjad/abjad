# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_KeySignature___repr___01():
    r'''Key signature returns nonempty string repr.
    '''

    result = repr(KeySignature('g', 'major'))
    assert isinstance(result, str) and 0 < len(result)
