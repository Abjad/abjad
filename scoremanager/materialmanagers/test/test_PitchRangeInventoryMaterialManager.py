# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_PitchRangeInventoryMaterialManager_01():
    r'''Stub material package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materials.testpir'
    assert not score_manager._configuration.package_exists(string)
    try:
        score_manager._run(pending_user_input=
            'lmm nmm pitch testpir default '
            'q'
            )
        #string = 'scoremanager.materials.testpir'
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testpir')
        manager = scoremanager.materialmanagers.PitchRangeInventoryMaterialManager(
            filesystem_path=path)
        assert manager._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            ]
        assert manager.output_material is None
    finally:
        string = 'lmm testpir rm default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materials.testpir'
        assert not score_manager._configuration.package_exists(string)


def test_PitchRangeInventoryMaterialManager_02():
    r'''Populate output material module.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materials.testpir'
    assert not score_manager._configuration.package_exists(string)
    try:
        score_manager._run(pending_user_input=
            'lmm nmm pitch testpir default '
            'testpir omi add [A0, C8] add [C2, F#5] add [C2, G5] '
            'rm 1 move 1 2 b default '
            'q'
            )
        #string = 'scoremanager.materials.testpir'
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testpir')
        manager = scoremanager.materialmanagers.PitchRangeInventoryMaterialManager(
            filesystem_path=path)
        assert manager._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'illustration_builder.py',
            'output_material.py',
            ]
        pitch_range_inventory = pitchtools.PitchRangeInventory([
            pitchtools.PitchRange('[C2, G5]'), 
            pitchtools.PitchRange('[C2, F#5]'),
            ])
        assert manager.output_material == pitch_range_inventory
    finally:
        string = 'lmm testpir rm default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materials.testpir'
        assert not score_manager._configuration.package_exists(string)
