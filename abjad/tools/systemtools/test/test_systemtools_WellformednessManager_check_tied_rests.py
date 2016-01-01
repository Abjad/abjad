# -*- coding: utf-8 -*-
from abjad import *


def test_systemtools_WellformednessManager_check_beamed_quarter_notes_01():
    r'''Tied rests are not well-formed.
    '''

    staff = Staff("r4 ~ r4")

    assert not inspect_(staff).is_well_formed()