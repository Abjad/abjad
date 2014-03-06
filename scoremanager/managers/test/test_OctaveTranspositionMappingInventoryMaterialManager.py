# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_OctaveTranspositionMappingInventoryMaterialManager_01():
    r'''Stub material package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.abjad_material_packages_directory_path,
        'testoctavetrans',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        ]
    input_ = 'lmm nmm octave testoctavetrans default q'

    try:
        score_manager._run(pending_user_input=input_, is_test=True)
        manager = scoremanager.managers.OctaveTranspositionMappingInventoryMaterialManager(
            path=path)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_material_module()
        assert output_material is None
    finally:
        input_ = 'lmm testoctavetrans rm remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(path)


def test_OctaveTranspositionMappingInventoryMaterialManager_02():
    r'''Populate output material module.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.abjad_material_packages_directory_path,
        'testoctavetrans',
        )
    assert not os.path.exists(path)
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'output_material.py',
        ]
    mapping_1 = pitchtools.OctaveTranspositionMapping([
        ('[A0, C4)', 15), 
        ('[C4, C8)', 27),
        ])
    mapping_2 = pitchtools.OctaveTranspositionMapping([
        ('[A0, C8]', -18),
        ])
    inventory = pitchtools.OctaveTranspositionMappingInventory([
        mapping_1, 
        mapping_2
        ])
    input_ = 'lmm nmm octave testoctavetrans'
    input_ += ' testoctavetrans omi add add source [A0, C4) target 15 done'
    input_ += ' add source [C4, C8) target 27 done done'
    input_ += ' add add source [A0, C8] target -18 done done done default q'

    try:
        score_manager._run(pending_user_input=input_, is_test=True)
        manager = scoremanager.managers.OctaveTranspositionMappingInventoryMaterialManager(
            path=path)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_material_module()
        assert output_material == inventory
    finally:
        string = 'lmm testoctavetrans rm remove q'
        score_manager._run(pending_user_input=string)
        assert not os.path.exists(path)
