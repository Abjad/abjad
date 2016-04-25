# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Leaf__multiplied_duration_01():
    r'''Mulplied duration == written * multiplier.
    '''

    note = Note("c'4")
    attach(Multiplier(1, 2), note)
    assert note._multiplied_duration == Duration(1, 8)


def test_scoretools_Leaf__multiplied_duration_02():
    r'''Mulplied duration equals duration when multiplier is none.
    '''

    note = Note("c'4")
    assert note._multiplied_duration == Duration(1, 4)


def test_scoretools_Leaf__multiplied_duration_03():
    r'''Attach multiplier and then detach multiplier.
    '''

    note = Note("c'4")
    note.written_duration = Duration(3, 8)
    attach(Multiplier(2, 3), note)

    assert note.written_duration == Duration(3, 8)
    assert inspect_(note).get_indicator(Multiplier) == Multiplier(2, 3)
    assert note._multiplied_duration == Duration(1, 4)

    note.written_duration = Duration(1, 4)
    detach(Multiplier, note)

    assert note.written_duration == Duration(1, 4)
    assert inspect_(note).get_indicators(Multiplier) == ()
    assert note._multiplied_duration == Duration(1, 4)
