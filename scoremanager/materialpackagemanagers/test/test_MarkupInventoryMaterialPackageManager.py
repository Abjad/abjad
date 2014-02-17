# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MarkupInventoryMaterialPackageManager_01():

    score_manager = scoremanager.core.ScoreManager()
    string = 'scoremanager.materialpackages.testmarkupinventory'
    assert not score_manager.configuration.packagesystem_path_exists(string)
    try:
        score_manager._run(pending_user_input=
            "materials nmm markup testmarkupinventory "
            "omi "
            "add arg r'\\italic~{~serenamente~}' done "
            "add arg r'\\italic~{~presto~}' done done default q"
            )
        string = 'scoremanager.materialpackages.testmarkupinventory'
        mpp = scoremanager.materialpackagemanagers.ArticulationHandlerMaterialPackageManager(
            string)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'illustration_builder.py',
            'output_material.py',
            ]
        inventory = markuptools.MarkupInventory([
            markuptools.Markup(
                '\\italic { serenamente }',
                ),
            markuptools.Markup(
                '\\italic { presto }',
                )
            ],
            )
        assert mpp.output_material == inventory
    finally:
        string = 'm testmarkupinventory del remove default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materialpackages.testmarkupinventory'
        assert not \
            score_manager.configuration.packagesystem_path_exists(string)
