# -*- coding: utf-8 -*-
import abjad
from abjad.tools import systemtools


def test_systemtools_WellformednessManager_check_beamed_quarter_notes_01():
    r'''Beamed quarter notes are not well-formed.

    Here the beam abjad.attaches directly to the quarter notes.
    '''

    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])

    assert not abjad.inspect(staff).is_well_formed()
