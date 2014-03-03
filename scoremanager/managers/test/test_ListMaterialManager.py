# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_ListMaterialManager_01():

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materials.testlist'
    assert not score_manager._configuration.package_exists(string)
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'output_material.py',
        ]

    try:
        score_manager._run(pending_user_input=
            'lmm nmm list testlist '
            "17 foo done b default q "
            )
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testlist')
        manager = scoremanager.managers.ListMaterialManager(path)
        assert manager._list_directory() == directory_entries
        output_material = manager._execute_output_material_module()
        assert output_material == [17, 'foo']
    finally:
        string = 'lmm testlist rm remove q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materials.testlist'
        assert not score_manager._configuration.package_exists(string)
