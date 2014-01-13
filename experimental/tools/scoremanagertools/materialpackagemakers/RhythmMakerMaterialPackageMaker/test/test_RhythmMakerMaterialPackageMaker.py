# -*- encoding: utf-8 -*-
from experimental import *


def test_RhythmMakerMaterialPackageMaker_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'experimental.tools.scoremanagertools.materialpackages.testrhythmmaker')
    try:
        score_manager._run(pending_user_input=
            'materials maker rhythm testrhythmmaker default '
            'testrhythmmaker omi burnishedtalearhythmmaker '
            '(-1, 2, -3, 4) 16 (2, 3) (6,) b default '
            'q '
            )
        mpp = scoremanagertools.materialpackagemakers.RhythmMakerMaterialPackageMaker(
            'experimental.tools.scoremanagertools.materialpackages.testrhythmmaker')
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'output_material.py',
            ]
        maker = rhythmmakertools.BurnishedTaleaRhythmMaker(
            talea=(-1, 2, -3, 4),
            talea_denominator=16,
            prolation_addenda=(2, 3),
            secondary_divisions=(6,),
            )
        assert mpp.output_material == maker
    finally:
        score_manager._run(pending_user_input=
            'm testrhythmmaker del remove default q',
            )
        assert not score_manager.configuration.packagesystem_path_exists(
            'experimental.tools.scoremanagertools.materialpackages.testrhythmmaker')
