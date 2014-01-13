# -*- encoding: utf-8 -*-
from experimental import *


def test_DivisionBurnishedTaleaRhythmMakerEditor_01():

    editor = scoremanagertools.editors.DivisionBurnishedTaleaRhythmMakerEditor()
    editor._run(pending_user_input=
        '1 (1, 1, 2, 4) 32 (0,) (-1,) (0,) (-1,) (2,) (1,) q', 
        is_autoadvancing=True,
        )

    maker = rhythmmakertools.DivisionBurnishedTaleaRhythmMaker(
        talea=(1, 1, 2, 4),
        talea_denominator=32,
        prolation_addenda=(0,),
        lefts=(-1,),
        middles=(0,),
        rights=(-1,),
        left_lengths=(2,),
        right_lengths=(1,),
        secondary_divisions=(),
        )

    assert editor.target == maker
