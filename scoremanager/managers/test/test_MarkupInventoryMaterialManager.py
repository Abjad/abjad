# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager


def test_MarkupInventoryMaterialManager_01():

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.abjad_material_packages_directory_path,
        'testmarkupinventory',
        )
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

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_, is_test=True)
        assert os.path.exists(path)
        manager = scoremanager.managers.ArticulationHandlerMaterialManager
        manager = manager(path=path)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_material_module()
        assert output_material == inventory
        input_ = 'lmm testmarkupinventory rm remove q'
        score_manager._run(pending_user_input=input_, is_test=True)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)
