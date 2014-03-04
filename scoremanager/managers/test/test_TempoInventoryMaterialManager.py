# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_TempoInventoryMaterialManager_01():

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materials.testtempoinventory'
    assert not score_manager._configuration.package_exists(string)
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'output_material.py', 
        ]
    inventory = indicatortools.TempoInventory([
        ((1, 4), 60), 
        ((1, 4), 90),
        ])

    try:
        score_manager._run(pending_user_input=
            'lmm nmm tempo testtempoinventory default '
            'testtempoinventory omi add ((1, 4), 60) add ((1, 4), 90) b default '
            'q '
            )
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testtempoinventory')
        manager = scoremanager.managers.TempoInventoryMaterialManager(
            path=path)
        assert manager._list_directory() == directory_entries
        output_material = manager._execute_output_material_module()
        assert output_material == inventory
    finally:
        string = 'lmm testtempoinventory rm remove q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materials.testtempoinventory'
        assert not score_manager._configuration.package_exists(string)
