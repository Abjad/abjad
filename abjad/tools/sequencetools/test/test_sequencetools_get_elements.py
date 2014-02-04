# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_get_elements_01():

    sequence = 'string of text'
    assert sequencetools.get_elements(sequence, (2, 3, 10, 12)) == (
        'r', 'i', 't', 'x')
