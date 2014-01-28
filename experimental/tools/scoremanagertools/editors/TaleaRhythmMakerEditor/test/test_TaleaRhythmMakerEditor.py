# -*- encoding: utf-8 -*-
from experimental import *


def test_TaleaRhythmMakerEditor_01():

    editor = scoremanagertools.editors.TaleaRhythmMakerEditor()
    editor._run(pending_user_input=
        '2 16 (2, 3) (6,) (-1, 2, -3, 4) q', 
        is_autoadvancing=True,
        )

    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=(-1, 2, -3, 4), 
        talea_denominator=16,
        extra_counts_per_division=(2, 3),
        split_divisions_every=(6,),
        )

    assert editor.target == maker
