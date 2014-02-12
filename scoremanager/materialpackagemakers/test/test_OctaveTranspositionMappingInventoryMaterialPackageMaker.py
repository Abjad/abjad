# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_OctaveTranspositionMappingInventoryMaterialPackageMaker_01():
    r'''Stub material package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanager.materialpackages.testoctavetrans')
    try:
        score_manager._run(pending_user_input=
            'materials maker octave testoctavetrans default '
            'q'
            )
        mpp = scoremanager.materialpackagemakers.OctaveTranspositionMappingInventoryMaterialPackageMaker('scoremanager.materialpackages.testoctavetrans')
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            ]
        assert mpp.output_material is None
    finally:
        score_manager._run(pending_user_input='m testoctavetrans del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testoctavetrans')


def test_OctaveTranspositionMappingInventoryMaterialPackageMaker_02():
    r'''Populate output material module.
    '''

    score_manager = scoremanager.core.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanager.materialpackages.testoctavetrans')
    try:
        score_manager._run(pending_user_input=
            'materials maker octave testoctavetrans '
            'testoctavetrans omi add add source [A0, C4) target 15 done '
            'add source [C4, C8) target 27 done done '
            'add add source [A0, C8] target -18 done done done default q'
            )
        mpp = scoremanager.materialpackagemakers.OctaveTranspositionMappingInventoryMaterialPackageMaker(
            'scoremanager.materialpackages.testoctavetrans')
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'output_material.py',
            ]
        mapping_1 = pitchtools.OctaveTranspositionMapping([('[A0, C4)', 15), ('[C4, C8)', 27)])
        mapping_2 = pitchtools.OctaveTranspositionMapping([('[A0, C8]', -18)])
        inventory = pitchtools.OctaveTranspositionMappingInventory([mapping_1, mapping_2])
        assert mpp.output_material == inventory
    finally:
        score_manager._run(pending_user_input='m testoctavetrans del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testoctavetrans')
