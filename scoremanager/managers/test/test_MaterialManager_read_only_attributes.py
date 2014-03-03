# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_MaterialManager_read_only_attributes_01():
    r'''Data-only package.
    '''

    string = 'scoremanager.materials.example_numbers'
    filesystem_path = os.path.join(
        configuration.abjad_material_packages_directory_path,
        'example_numbers',
        )
    manager = scoremanager.managers.MaterialManager(filesystem_path)
    assert manager._breadcrumb == 'example numbers'
    assert os.path.isfile(manager._material_definition_module_path)
    assert not manager._read_material_manager_class_name()
    material_definition = manager._execute_material_definition_module()
    assert material_definition == [1, 2, 3, 4, 5]


def test_MaterialManager_read_only_attributes_02():
    r'''Makermade material.
    '''

    string = 'scoremanager.materials.example_sargasso_measures'
    filesystem_path = os.path.join(
        configuration.abjad_material_packages_directory_path,
        'example_sargasso_measures',
        )
    manager = scoremanager.managers.SargassoMeasureMaterialManager(
        filesystem_path=filesystem_path,    
        )
    assert manager._breadcrumb == 'example sargasso measures'
    assert not os.path.isfile(manager._material_definition_module_path)
    assert manager._read_material_manager_class_name()


def test_MaterialManager_read_only_attributes_03():
    r'''Handmade material.
    '''

    string = 'scoremanager.materials.example_notes'
    filesystem_path = os.path.join(
        configuration.abjad_material_packages_directory_path,
        'example_notes',
        )
    manager = scoremanager.managers.MaterialManager(filesystem_path)
    assert manager._breadcrumb == 'example notes'
    assert not manager._read_material_manager_class_name()
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'example_notes', 
        'illustration_builder.py',
        )
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'example_notes',
        )
    material_definition = manager._execute_material_definition_module()
    assert all(isinstance(x, Note) for x in material_definition)
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'example_notes', 
        'output_material.py',
        )
