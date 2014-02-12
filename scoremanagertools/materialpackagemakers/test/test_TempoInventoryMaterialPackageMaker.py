# -*- encoding: utf-8 -*-
from experimental import *


def test_TempoInventoryMaterialPackageMaker_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanagertools.materialpackages.testtempoinventory')
    try:
        score_manager._run(pending_user_input=
            'materials maker tempo testtempoinventory default '
            'testtempoinventory omi add ((1, 4), 60) add ((1, 4), 90) b default '
            'q '
            )
        mpp = scoremanagertools.materialpackagemakers.TempoInventoryMaterialPackageMaker(
            'scoremanagertools.materialpackages.testtempoinventory')
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'output_material.py', 
            ]
        inventory = indicatortools.TempoInventory([((1, 4), 60), ((1, 4), 90)])
        assert mpp.output_material == inventory
    finally:
        score_manager._run(pending_user_input='m testtempoinventory del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanagertools.materialpackages.testtempoinventory')
