# -*- encoding: utf-8 -*-
import pytest
from experimental import *
pytest.skip('unskip once it is possible to edit composite objects.')


def test_RhythmMakerMaterialPackageMaker_01():

    score_manager = scoremanagertools.core.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanagertools.materialpackages.testrhythmmaker')
    try:
        score_manager._run(pending_user_input=
            'materials maker rhythm testrhythmmaker default '
            'testrhythmmaker omi talearhythmmaker '
            '(-1, 2, -3, 4) 16 (2, 3) (6,) b default '
            'q '
            )
        mpp = scoremanagertools.materialpackagemakers.RhythmMakerMaterialPackageMaker(
            'scoremanagertools.materialpackages.testrhythmmaker')
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
        score_manager._run(pending_user_input=
            'm testrhythmmaker del remove default q',
            )
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanagertools.materialpackages.testrhythmmaker')
