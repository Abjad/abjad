# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager
pytest.skip('unskip once it is possible to edit composite objects.')


def test_RhythmMakerMaterialPackageMaker_01():

    score_manager = scoremanager.core.ScoreManager()
    string = 'scoremanager.materialpackages.testrhythmmaker'
    assert not score_manager.configuration.packagesystem_path_exists(string)
    try:
        score_manager._run(pending_user_input=
            'materials maker rhythm testrhythmmaker default '
            'testrhythmmaker omi talearhythmmaker '
            '(-1, 2, -3, 4) 16 (2, 3) (6,) b default '
            'q '
            )
        string = 'scoremanager.materialpackages.testrhythmmaker'
        mpp = scoremanager.materialpackagemanagers.RhythmMakerMaterialPackageMaker(
            string)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'output_material.py',
            ]
        talea = rhythmmakertools.Talea(
            counts=(-1, 2, -3, 4),
            denominator=16,
            )
        maker = rhythmmakertools.TaleaRhythmMaker(
            talea=talea,
            extra_counts_per_division=(2, 3),
            split_divisions_by_counts=(6,),
            )
        assert mpp.output_material == maker
    finally:
        string = 'm testrhythmmaker del remove default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materialpackages.testrhythmmaker'
        assert not \
            score_manager.configuration.packagesystem_path_exists(string)
