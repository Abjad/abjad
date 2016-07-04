# -*- coding: utf-8 -*-
from abjad import *


def test_systemtools_WellformednessManager_check_beamed_quarter_notes_01():
    r'''Beamed quarter notes are not well-formed.

    Here the beam attaches directly to the quarter notes.
    '''

    staff = Staff("c'4 d'4 e'4 f'4")
    beam = Beam()
    attach(beam, staff[:])

    assert not inspect_(staff).is_well_formed()