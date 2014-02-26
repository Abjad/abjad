# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager
pytest.skip('unskip once it is possible to edit composite objects.')


def test_RhythmMakerMaterialPackageManager_01():

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materialpackages.testrhythmmaker'
    assert not score_manager._configuration.package_exists(string)
    try:
        score_manager._run(pending_user_input=
            'lmm nmm rhythm testrhythmmaker default '
            'testrhythmmaker omi talearhythmmaker '
            '(-1, 2, -3, 4) 16 (2, 3) (6,) b default '
            'q '
            )
        #string = 'scoremanager.materialpackages.testrhythmmaker'
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testrhythmmaker')
        manager = scoremanager.materialmanagers.RhythmMakerMaterialPackageManager(
            filesystem_path=path)
        assert manager._list_directory() == [
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
        assert manager.output_material == maker
    finally:
        string = 'lmm testrhythmmaker rm default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materialpackages.testrhythmmaker'
        assert not score_manager._configuration.package_exists(string)
