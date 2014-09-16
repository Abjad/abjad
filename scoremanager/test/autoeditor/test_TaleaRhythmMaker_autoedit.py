# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_TaleaRhythmMaker_autoedit_01():
    r'''Edits talea rhythm-maker.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    target = rhythmmakertools.TaleaRhythmMaker()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 't c (-1, 2, -3, 4) d 16 done sd/ (6,) (2, 3)/ done'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    talea = rhythmmakertools.Talea(
        counts=(-1, 2, -3, 4),
        denominator=16,
        )

    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        split_divisions_by_counts=(6,),
        extra_counts_per_division=(2, 3),
        )

    assert autoeditor.target == maker