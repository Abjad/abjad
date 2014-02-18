# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PitchRangeInventoryMaterialPackageManager_01():
    r'''Stub material package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'scoremanager.materialpackages.testpir'
    assert not score_manager.configuration.packagesystem_path_exists(string)
    try:
        score_manager._run(pending_user_input=
            'lmm nmm pitch testpir default '
            'q'
            )
        string = 'scoremanager.materialpackages.testpir'
        mpp = scoremanager.materialpackagemanagers.PitchRangeInventoryMaterialPackageManager(
            string)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            ]
        assert mpp.output_material is None
    finally:
        string = 'lmm testpir del remove default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materialpackages.testpir'
        assert not \
            score_manager.configuration.packagesystem_path_exists(string)


def test_PitchRangeInventoryMaterialPackageManager_02():
    r'''Populate output material module.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'scoremanager.materialpackages.testpir'
    assert not score_manager.configuration.packagesystem_path_exists(string)
    try:
        score_manager._run(pending_user_input=
            'lmm nmm pitch testpir default '
            'testpir omi add [A0, C8] add [C2, F#5] add [C2, G5] '
            'rm 1 move 1 2 b default '
            'q'
            )
        string = 'scoremanager.materialpackages.testpir'
        mpp = scoremanager.materialpackagemanagers.PitchRangeInventoryMaterialPackageManager(
            string)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'illustration_builder.py',
            'output_material.py',
            ]
        pitch_range_inventory = pitchtools.PitchRangeInventory([
            pitchtools.PitchRange('[C2, G5]'), 
            pitchtools.PitchRange('[C2, F#5]'),
            ])
        assert mpp.output_material == pitch_range_inventory
    finally:
        string = 'lmm testpir del remove default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materialpackages.testpir'
        assert not \
            score_manager.configuration.packagesystem_path_exists(string)
