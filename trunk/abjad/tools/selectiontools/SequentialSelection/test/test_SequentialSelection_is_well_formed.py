# -*- encoding: utf-8 -*-
from abjad import *


def test_SequentialSelection_is_well_formed_01():
    r'''Well-formedness checking runs correctly against leaves.
    '''
    t = Note("c'4")
    assert select(t).is_well_formed()


def test_SequentialSelection_is_well_formed_02():
    r'''Well-formedness checking runs correctly against containers.
    '''
    t = Staff([Note(n, (1, 8)) for n in range(8)])
    assert select(t).is_well_formed()
