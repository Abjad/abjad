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
    assert not manager.has_illustration_builder_module
    assert not manager.has_illustration_ly
    assert not manager.has_illustration_pdf
    assert manager.has_material_definition
    assert manager.has_material_definition_module
    assert not manager.has_material_package_manager
    assert manager.has_output_material
    assert manager.has_output_material_module
    assert not manager.has_user_input_module
    assert not manager.has_user_input_wrapper_on_disk
    assert manager.material_definition == [1, 2, 3, 4, 5]
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'example_numbers', 
        'material_definition.py',
        )
    assert manager.material_definition_module_path == file_path
    string = 'scoremanager.materials.example_numbers.material_definition'
    assert manager.material_definition_package_path == string
    directory_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'example_numbers',
        )
    assert manager.material_package_directory == directory_path
    assert manager.material_package_manager is None
    assert manager.material_package_manager_class_name is None
    assert manager.material_package_name == 'example_numbers'
    assert manager.space_delimited_material_package_name == 'example numbers'
    assert manager.material_package_name == 'example_numbers'
    result = ['example_numbers = [1, 2, 3, 4, 5]']
    assert manager.output_material_module_body_lines == result
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'example_numbers', 
        'output_material.py',
        )
    assert manager.output_material_module_path == file_path
    assert manager.output_material_module_manager is not None
    assert manager.stylesheet_file_path_on_disk is None
    assert manager.user_input_module_path is None
    assert manager.user_input_module_package is None


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
    assert manager.has_illustration_builder_module
    assert manager.has_illustration_ly
    assert manager.has_illustration_pdf
    assert not manager.has_material_definition
    assert not manager.has_material_definition_module
    assert manager.has_material_package_manager
    assert manager.has_output_material
    assert manager.has_output_material_module
    assert manager.has_user_input_module
    assert manager.has_user_input_wrapper_on_disk
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'example_sargasso_measures', 
        'illustration.ly',
        )
    assert manager.illustration_ly_file_path == file_path
    assert manager.illustration_ly_file_manager is not None
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'example_sargasso_measures', 
        'illustration.pdf',
        )
    assert manager.illustration_pdf_file_path == file_path
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'example_sargasso_measures',
        )
    assert manager.material_package_directory == file_path
    maker = scoremanager.managers.SargassoMeasureMaterialManager
    assert manager.material_package_manager is maker
    string = 'SargassoMeasureMaterialManager'
    assert manager.material_package_manager_class_name == string
    assert manager.material_package_name == 'example_sargasso_measures'
    string = 'example sargasso measures'
    assert manager.space_delimited_material_package_name == string
    assert manager.material_package_name == 'example_sargasso_measures'
    assert manager.output_material_module_body_lines is None
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'example_sargasso_measures', 
        'output_material.py',
        )
    assert manager.output_material_module_path == file_path
    assert manager.output_material_module_manager is not None
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'example_sargasso_measures', 
        'user_input.py',
        )
    assert manager.user_input_module_path == file_path
    string = 'scoremanager.materials.example_sargasso_measures.user_input'
    assert manager.user_input_module_package == string


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
    assert manager.has_illustration_builder_module
    assert manager.has_illustration_ly
    assert manager.has_illustration_pdf
    assert manager.has_material_definition
    assert manager.has_material_definition_module
    assert not manager.has_material_package_manager
    assert manager.has_output_material
    assert manager.has_output_material_module
    assert not manager.has_user_input_module
    assert not manager.has_user_input_wrapper_on_disk
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'example_notes', 
        'illustration_builder.py',
        )
    assert manager.illustration_builder_module_path == file_path
    string = 'scoremanager.materials.example_notes.illustration_builder'
    assert manager.illustration_builder_package_path == string
    assert manager.illustration_builder_module_manager is not None
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'example_notes', 
        'illustration.ly',
        )
    assert manager.illustration_ly_file_path == file_path
    assert manager.illustration_ly_file_manager is not None
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'example_notes', 
        'illustration.pdf',
        )
    assert manager.illustration_pdf_file_path == file_path
    assert manager.illustration_pdf_file_manager is not None
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'example_notes', 
        'material_definition.py',
        )
    assert manager.material_definition_module_path == file_path
    string = 'scoremanager.materials.example_notes.material_definition'
    assert manager.material_definition_package_path == string
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'example_notes',
        )
    assert manager.material_package_directory == file_path
    assert manager.material_package_manager is None
    assert manager.material_package_manager_class_name is None
    assert manager.material_package_name == 'example_notes'
    assert manager.space_delimited_material_package_name == 'example notes'
    assert manager.material_package_name == 'example_notes'
    assert all(isinstance(x, Note) for x in manager.material_definition)
    assert manager.output_material_module_body_lines is not None
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'example_notes', 
        'output_material.py',
        )
    assert manager.output_material_module_path == file_path
    assert manager.output_material_module_manager is not None
