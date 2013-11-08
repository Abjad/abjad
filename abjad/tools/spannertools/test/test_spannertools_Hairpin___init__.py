# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_Hairpin___init___01():
    r'''Init empty hairpin spanner.
    '''

    hairpin = Hairpin()
    assert isinstance(hairpin, Hairpin)
