# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager


def test_TempoInventoryMaterialManager_edit_output_material_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testtempoinventory',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'output_material.py', 
        ]
    inventory = indicatortools.TempoInventory([
        ((1, 4), 60), 
        ((1, 4), 90),
        ])
    input_ = 'lmm nmm tempo testtempoinventory default testtempoinventory me'
    input_ += ' add ((1, 4), 60) add ((1, 4), 90) b default q'

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.TempoInventoryMaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_module()
        assert output_material == inventory
        input_ = 'lmm testtempoinventory rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)
