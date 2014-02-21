# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ListMaterialPackageManager_01():

    score_manager = scoremanager.core.ScoreManager()
    string = 'scoremanager.materialpackages.testlist'
    assert not score_manager.configuration.package_path_exists(string)
    try:
        score_manager._run(pending_user_input=
            'lmm nmm list testlist '
            "17 foo done b default q "
            )
        string = 'scoremanager.materialpackages.testlist'
        mpp = \
            scoremanager.materialpackagemanagers.ListMaterialPackageManager(string)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'illustration_builder.py',
            'output_material.py',
            ]
        assert mpp.output_material == [17, 'foo']
    finally:
        string = 'lmm testlist del remove default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materialpackages.testlist'
        assert not \
            score_manager.configuration.package_path_exists(string)
