# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_TempoInventoryMaterialManager_01():

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materials.testtempoinventory'
    assert not score_manager._configuration.package_exists(string)
    try:
        score_manager._run(pending_user_input=
            'lmm nmm tempo testtempoinventory default '
            'testtempoinventory omi add ((1, 4), 60) add ((1, 4), 90) b default '
            'q '
            )
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testtempoinventory')
        manager = scoremanager.managers.TempoInventoryMaterialManager(
            filesystem_path=path)
        assert manager._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'output_material.py', 
            ]
        inventory = indicatortools.TempoInventory([((1, 4), 60), ((1, 4), 90)])
        assert manager.output_material == inventory
    finally:
        string = 'lmm testtempoinventory rm default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materials.testtempoinventory'
        assert not score_manager._configuration.package_exists(string)
