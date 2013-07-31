# -*- encoding: utf-8 -*-
from abjad import *


def test_KeySignatureMark___repr___01():
    r'''Key signature returns nonempty string repr.
    '''

    repr = contexttools.KeySignatureMark('g', 'major').__repr__()
    assert isinstance(repr, str) and 0 < len(repr)
