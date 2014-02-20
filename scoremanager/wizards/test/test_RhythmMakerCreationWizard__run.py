# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager
pytest.skip('unskip once it is possible to edit composite objects.')


def test_RhythmMakerCreationWizard__run_01():

    wizard = scoremanager.wizards.RhythmMakerCreationWizard()
    wizard._run(pending_user_input=
        'talearhythmmaker (-1, 2, -3, 4) 16 (2, 3) (6,) b'
        )

    talea = rhythmmakertools.Talea(
        counts=(-1, 2, -3, 4),
        denominator=16,
        )
        
    maker = rhythmmakertools.TaleaRhythmMaker(
        talea=talea,
        extra_counts_per_division=(2, 3),
        split_divisions_by_counts=(6,),
        )

    assert wizard.target == maker
