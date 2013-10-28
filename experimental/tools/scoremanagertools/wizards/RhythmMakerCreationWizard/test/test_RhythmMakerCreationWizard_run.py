# -*- encoding: utf-8 -*-
from abjad.tools import rhythmmakertools
from experimental import *
import py.test


@py.test.skip('FIXME: Broken by class package flattening.')
def test_RhythmMakerCreationWizard_run_01():

    wizard = scoremanagertools.wizards.RhythmMakerCreationWizard()
    wizard._run(pending_user_input='talearhythmmaker [-1, 2, -3, 4] 16 [2, 3] [6] b')

    maker = rhythmmakertools.TaleaRhythmMaker(
        [-1, 2, -3, 4],
        16,
        prolation_addenda=[2, 3],
        secondary_divisions=[6],
        )

    assert wizard.target == maker
