# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager
pytest.skip('unskip once it is possible to edit composite objects.')


def test_TaleaRhythmMakerEditor__run_01():

    session = scoremanager.core.Session(is_test=True)
    editor = scoremanager.editors.TaleaRhythmMakerEditor(session=session)
    input_ = '2 16 (2, 3) (6,) (-1, 2, -3, 4) q' 
    editor._run(pending_user_input=input_, is_autoadvancing=True)

    talea = rhythmmakertools.Talea(
        counts=(-1, 2, -3, 4), 
        denominator=16,
        )

    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        extra_counts_per_division=(2, 3),
        split_divisions_by_counts=(6,),
        )

    assert editor.target == maker
