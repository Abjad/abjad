# -*- encoding: utf-8 -*-
from experimental import *


def test_RhythmMakerCreationWizard_run_01():

    wizard = scoremanagertools.wizards.RhythmMakerCreationWizard()
    wizard._run(pending_user_input=
        'talearhythmmaker (-1, 2, -3, 4) 16 (2, 3) (6,) b'
        )

    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=(-1, 2, -3, 4),
        talea_denominator=16,
        extra_counts_per_division=(2, 3),
        split_divisions_every=(6,),
        )

    assert wizard.target == maker
