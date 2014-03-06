# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_MarkupInventoryMaterialManager_01():

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.abjad_material_packages_directory_path,
        'testmarkupinventory',
        )
    assert not os.path.exists(path)
    inventory = markuptools.MarkupInventory(
        [
            markuptools.Markup(
                '\\italic { serenamente }',
                ),
            markuptools.Markup(
                '\\italic { presto }',
                )
            ],
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'output_material.py',
        ]
    input_ = "lmm nmm markup testmarkupinventory omi"
    input_ += " add arg r'\\italic~{~serenamente~}' done"
    input_ += " add arg r'\\italic~{~presto~}' done done default q"

    try:
        score_manager._run(pending_user_input=input_)
        manager = scoremanager.managers.ArticulationHandlerMaterialManager(
            path=path)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_material_module()
        assert output_material == inventory
    finally:
        input_ = 'lmm testmarkupinventory rm remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(path)
