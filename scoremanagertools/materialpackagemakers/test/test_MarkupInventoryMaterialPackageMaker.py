# -*- encoding: utf-8 -*-
from experimental import *


def test_MarkupInventoryMaterialPackageMaker_01():

    score_manager = scoremanagertools.core.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanagertools.materialpackages.testmarkupinventory')
    try:
        score_manager._run(pending_user_input=
            "materials maker markup testmarkupinventory "
            "omi name test~markup~inventory "
            "add arg r'\\italic~{~serenamente~}' name serenamente done "
            "add arg r'\\italic~{~presto~}' name presto done done default q"
            )
        mpp = scoremanagertools.materialpackagemakers.ArticulationHandlerMaterialPackageMaker(
            'scoremanagertools.materialpackages.testmarkupinventory')
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
        score_manager._run(pending_user_input='m testmarkupinventory del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanagertools.materialpackages.testmarkupinventory')
