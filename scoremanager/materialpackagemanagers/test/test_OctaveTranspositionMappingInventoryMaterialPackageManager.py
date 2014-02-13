# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_OctaveTranspositionMappingInventoryMaterialPackageManager_01():
    r'''Stub material package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'scoremanager.materialpackages.testoctavetrans'
    assert not score_manager.configuration.packagesystem_path_exists(string)
    try:
        score_manager._run(pending_user_input=
            'materials maker octave testoctavetrans default '
            'q'
            )
        string = 'scoremanager.materialpackages.testoctavetrans'
        mpp = scoremanager.materialpackagemanagers.OctaveTranspositionMappingInventoryMaterialPackageManager(
            string)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            ]
        assert mpp.output_material is None
    finally:
        string = 'm testoctavetrans del remove default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materialpackages.testoctavetrans'
        assert not \
            score_manager.configuration.packagesystem_path_exists(string)


def test_OctaveTranspositionMappingInventoryMaterialPackageManager_02():
    r'''Populate output material module.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'scoremanager.materialpackages.testoctavetrans'
    assert not score_manager.configuration.packagesystem_path_exists(string)
    try:
        score_manager._run(pending_user_input=
            'materials maker octave testoctavetrans '
            'testoctavetrans omi add add source [A0, C4) target 15 done '
            'add source [C4, C8) target 27 done done '
            'add add source [A0, C8] target -18 done done done default q'
            )
        string = 'scoremanager.materialpackages.testoctavetrans'
        mpp = scoremanager.materialpackagemanagers.OctaveTranspositionMappingInventoryMaterialPackageManager(
            string)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'illustration_builder.py',
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
        assert mpp.output_material == inventory
    finally:
        string = 'm testoctavetrans del remove default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materialpackages.testoctavetrans'
        assert not \
            score_manager.configuration.packagesystem_path_exists(string)
