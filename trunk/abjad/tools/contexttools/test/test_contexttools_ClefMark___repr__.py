# -*- encoding: utf-8 -*-
from abjad import *


def test_contexttools_ClefMark___repr___01():
    r'''Clef returns a nonempty repr string.
    '''

    repr = contexttools.ClefMark('treble').__repr__()
    assert isinstance(repr, str) and 0 < len(repr)
