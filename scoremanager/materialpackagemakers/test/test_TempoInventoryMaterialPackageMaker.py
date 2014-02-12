# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_TempoInventoryMaterialPackageMaker_01():

    score_manager = scoremanager.core.ScoreManager()
    string = 'scoremanager.materialpackages.testtempoinventory'
    assert not score_manager.configuration.packagesystem_path_exists(string)
    try:
        score_manager._run(pending_user_input=
            'materials maker tempo testtempoinventory default '
            'testtempoinventory omi add ((1, 4), 60) add ((1, 4), 90) b default '
            'q '
            )
        string = 'scoremanager.materialpackages.testtempoinventory'
        mpp = scoremanager.materialpackagemakers.TempoInventoryMaterialPackageMaker(
            string)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'illustration_builder.py',
            'output_material.py', 
            ]
        inventory = indicatortools.TempoInventory([((1, 4), 60), ((1, 4), 90)])
        assert mpp.output_material == inventory
    finally:
        string = 'm testtempoinventory del remove default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materialpackages.testtempoinventory'
        assert not \
            score_manager.configuration.packagesystem_path_exists(string)
