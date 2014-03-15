# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager


def test_PitchRangeInventoryMaterialManager_edit_output_material_01():
    r'''Stub material package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testpir',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        ]
    input_ = 'lmm nmm pitch testpir default q'

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_, is_test=True)
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.PitchRangeInventoryMaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_module()
        assert output_material is None
        input_ = 'lmm testpir rm remove q'
        score_manager._run(pending_user_input=input_, is_test=True)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_PitchRangeInventoryMaterialManager_edit_output_material_02():
    r'''Populate output material module.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testpir',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'output_material.py',
        ]
    inventory = pitchtools.PitchRangeInventory([
        pitchtools.PitchRange('[C2, G5]'), 
        pitchtools.PitchRange('[C2, F#5]'),
        ])
    input_ = 'lmm nmm pitch testpir default'
    input_ += ' testpir me add [A0, C8] add [C2, F#5] add [C2, G5]'
    input_ += ' rm 1 mv 1 2 b default q'

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_, is_test=True)
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.PitchRangeInventoryMaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_module()
        assert output_material == inventory
        input_ = 'lmm testpir rm remove q'
        score_manager._run(pending_user_input=input_, is_test=True)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)
