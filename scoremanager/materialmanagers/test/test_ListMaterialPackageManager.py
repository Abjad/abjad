# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_ListMaterialPackageManager_01():

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materialpackages.testlist'
    assert not score_manager._configuration.package_exists(string)
    try:
        score_manager._run(pending_user_input=
            'lmm nmm list testlist '
            "17 foo done b default q "
            )
        #string = 'scoremanager.materialpackages.testlist'
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testlist')
        manager = \
            scoremanager.materialmanagers.ListMaterialPackageManager(
                filesystem_path=path)
        assert manager._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'illustration_builder.py',
            'output_material.py',
            ]
        assert manager.output_material == [17, 'foo']
    finally:
        string = 'lmm testlist rm default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materialpackages.testlist'
        assert not score_manager._configuration.package_exists(string)
