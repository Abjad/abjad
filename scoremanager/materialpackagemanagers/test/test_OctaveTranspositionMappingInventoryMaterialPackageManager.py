# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_OctaveTranspositionMappingInventoryMaterialPackageManager_01():
    r'''Stub material package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materialpackages.testoctavetrans'
    assert not score_manager._configuration.package_exists(string)
    try:
        score_manager._run(pending_user_input=
            'lmm nmm octave testoctavetrans default '
            'q'
            )
        #string = 'scoremanager.materialpackages.testoctavetrans'
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testoctavetrans')
        manager = scoremanager.materialpackagemanagers.OctaveTranspositionMappingInventoryMaterialPackageManager(
            filesystem_path=path)
        assert manager._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            ]
        assert manager.output_material is None
    finally:
        string = 'lmm testoctavetrans rm default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materialpackages.testoctavetrans'
        assert not score_manager._configuration.package_exists(string)


def test_OctaveTranspositionMappingInventoryMaterialPackageManager_02():
    r'''Populate output material module.
    '''

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materialpackages.testoctavetrans'
    assert not score_manager._configuration.package_exists(string)
    try:
        score_manager._run(pending_user_input=
            'lmm nmm octave testoctavetrans '
            'testoctavetrans omi add add source [A0, C4) target 15 done '
            'add source [C4, C8) target 27 done done '
            'add add source [A0, C8] target -18 done done done default q'
            )
        #string = 'scoremanager.materialpackages.testoctavetrans'
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testoctavetrans')
        manager = scoremanager.materialpackagemanagers.OctaveTranspositionMappingInventoryMaterialPackageManager(
            filesystem_path=path)
        assert manager._list_directory() == [
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
        assert manager.output_material == inventory
    finally:
        string = 'lmm testoctavetrans rm default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materialpackages.testoctavetrans'
        assert not score_manager._configuration.package_exists(string)
