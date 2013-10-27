# -*- encoding: utf-8 -*-
from abjad import *


def test_selectiontools_SliceSelection_is_well_formed_01():
    r'''Well-formedness checking runs correctly against leaves.
    '''
    note = Note("c'4")
    assert inspect(note).is_well_formed()


def test_selectiontools_SliceSelection_is_well_formed_02():
    r'''Well-formedness checking runs correctly against containers.
    '''
    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    assert inspect(staff).is_well_formed()
