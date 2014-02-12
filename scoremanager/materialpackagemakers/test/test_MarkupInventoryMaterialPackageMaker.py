# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MarkupInventoryMaterialPackageMaker_01():

    score_manager = scoremanager.core.ScoreManager()
    string = 'scoremanager.materialpackages.testmarkupinventory'
    assert not score_manager.configuration.packagesystem_path_exists(string)
    try:
        score_manager._run(pending_user_input=
            "materials maker markup testmarkupinventory "
            "omi name test~markup~inventory "
            "add arg r'\\italic~{~serenamente~}' name serenamente done "
            "add arg r'\\italic~{~presto~}' name presto done done default q"
            )
        string = 'scoremanager.materialpackages.testmarkupinventory'
        mpp = scoremanager.materialpackagemakers.ArticulationHandlerMaterialPackageMaker(
            string)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'output_material.py',
            ]
        inventory = markuptools.MarkupInventory([
            markuptools.Markup(
                '\\italic { serenamente }',
                markup_name='serenamente'
                ),
            markuptools.Markup(
                '\\italic { presto }',
                markup_name='presto'
                )
            ],
            custom_identifier='test markup inventory'
            )
        assert mpp.output_material == inventory
    finally:
        string = 'm testmarkupinventory del remove default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materialpackages.testmarkupinventory'
        assert not \
            score_manager.configuration.packagesystem_path_exists(string)
