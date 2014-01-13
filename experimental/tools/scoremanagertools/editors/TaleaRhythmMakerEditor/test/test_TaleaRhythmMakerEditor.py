# -*- encoding: utf-8 -*-
from experimental import *


def test_BurnishedTaleaRhythmMakerEditor_01():

    editor = scoremanagertools.editors.BurnishedTaleaRhythmMakerEditor()
    editor._run(pending_user_input=
        '2 16 (2, 3) (6,) (-1, 2, -3, 4) q', 
        is_autoadvancing=True,
        )

    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=(-1, 2, -3, 4), 
        talea_denominator=16,
        prolation_addenda=(2, 3),
        secondary_divisions=(6,),
        )

    assert editor.target == maker
