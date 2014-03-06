# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_PitchRangeInventoryMaterialManager_01():
    r'''Stub material package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.abjad_material_packages_directory_path,
        'testpir',
        )
    assert not os.path.exists(path)
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        ]
    input_ = 'lmm nmm pitch testpir default q'

    try:
        score_manager._run(pending_user_input=input_, is_test=True)
        manager = scoremanager.managers.PitchRangeInventoryMaterialManager(
            path=path)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_material_module()
        assert output_material is None
    finally:
        input_ = 'lmm testpir rm remove q'
        score_manager._run(pending_user_input=input_, is_test=True)
        assert not os.path.exists(path)


def test_PitchRangeInventoryMaterialManager_02():
    r'''Populate output material module.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.abjad_material_packages_directory_path,
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
    input_ += ' testpir omi add [A0, C8] add [C2, F#5] add [C2, G5]'
    input_ += ' rm 1 mv 1 2 b default q'

    try:
        score_manager._run(pending_user_input=input_, is_test=True)
        manager = scoremanager.managers.PitchRangeInventoryMaterialManager(
            path=path)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_material_module()
        assert output_material == inventory
    finally:
        input_ = 'lmm testpir rm remove q'
        score_manager._run(pending_user_input=input_, is_test=True)
        assert not os.path.exists(path)
