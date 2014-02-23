# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_MaterialPackageManager_read_only_attributes_01():
    r'''Data-only package.
    '''

    string = 'scoremanager.materialpackages.red_numbers'
    manager = scoremanager.managers.MaterialPackageManager(string)
    assert manager._breadcrumb == 'red numbers'
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
    assert manager.illustration_builder_module_file_path is None
    assert manager.illustration_builder_package_path is None
    assert manager.illustration_ly_file_path is None
    assert manager.illustration_pdf_file_path is None
    assert manager.is_handmade
    assert manager.material_definition == [1, 2, 3, 4, 5]
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'red_numbers', 
        'material_definition.py',
        )
    assert manager.material_definition_module_file_path == file_path
    string = 'scoremanager.materialpackages.red_numbers.material_definition'
    assert manager.material_definition_package_path == string
    directory_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'red_numbers',
        )
    assert manager.material_package_directory == directory_path
    assert manager.material_package_manager is None
    assert manager.material_package_manager_class_name is None
    assert manager.material_package_name == 'red_numbers'
    assert manager.space_delimited_material_package_name == 'red numbers'
    assert manager.material_package_name == 'red_numbers'
    result = ['red_numbers = [1, 2, 3, 4, 5]']
    assert manager.output_material_module_body_lines == result
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'red_numbers', 
        'output_material.py',
        )
    assert manager.output_material_module_file_path == file_path
    string = 'scoremanager.materialpackages.red_numbers.output_material'
    assert manager.output_material_module_path == string
    assert manager.output_material_module_manager is not None
    assert not manager.should_have_illustration
    assert not manager.should_have_illustration_builder_module
    assert not manager.should_have_illustration_ly
    assert not manager.should_have_illustration_pdf
    assert manager.should_have_material_definition_module
    assert manager.should_have_output_material_module
    assert not manager.should_have_user_input_module
    assert manager.stylesheet_file_path_on_disk is None
    assert manager.user_input_module_file_path is None
    assert manager.user_input_module_package_path is None


def test_MaterialPackageManager_read_only_attributes_02():
    r'''Makermade material.
    '''

    string = 'scoremanager.materialpackages.red_sargasso_measures'
    manager = \
        scoremanager.materialpackagemanagers.SargassoMeasureMaterialPackageManager(
            string
            )
    assert manager._breadcrumb == 'red sargasso measures'
    assert not manager.has_illustration_builder_module
    assert manager.has_illustration_ly
    assert manager.has_illustration_pdf
    assert not manager.has_material_definition
    assert not manager.has_material_definition_module
    assert manager.has_material_package_manager
    assert manager.has_output_material
    assert manager.has_output_material_module
    assert manager.has_user_input_module
    assert manager.has_user_input_wrapper_on_disk
    assert manager.has_user_input_wrapper_in_memory
    assert manager.illustration_builder_module_file_path is None
    assert manager.illustration_builder_package_path is None
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'red_sargasso_measures', 
        'illustration.ly',
        )
    assert manager.illustration_ly_file_path == file_path
    assert manager.illustration_ly_file_manager is not None
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'red_sargasso_measures', 
        'illustration.pdf',
        )
    assert manager.illustration_pdf_file_path == file_path
    assert not manager.is_handmade
    assert manager.is_managermade
    assert manager.material_definition_module_file_path is None
    assert manager.material_definition_package_path is None
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'red_sargasso_measures',
        )
    assert manager.material_package_directory == file_path
    maker = scoremanager.materialpackagemanagers.SargassoMeasureMaterialPackageManager
    assert manager.material_package_manager is maker
    string = 'SargassoMeasureMaterialPackageManager'
    assert manager.material_package_manager_class_name == string
    assert manager.material_package_name == 'red_sargasso_measures'
    string = 'red sargasso measures'
    assert manager.space_delimited_material_package_name == string
    assert manager.material_package_name == 'red_sargasso_measures'
    assert manager.output_material_module_body_lines is None
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'red_sargasso_measures', 
        'output_material.py',
        )
    assert manager.output_material_module_file_path == file_path
    string = 'scoremanager.materialpackages.red_sargasso_measures.output_material'
    assert manager.output_material_module_path == string
    assert manager.output_material_module_manager is not None
    assert manager.should_have_illustration
    assert not  manager.should_have_illustration_builder_module
    assert manager.should_have_illustration_ly
    assert manager.should_have_illustration_pdf
    assert not  manager.should_have_material_definition_module
    assert manager.should_have_output_material_module
    assert manager.should_have_user_input_module
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'red_sargasso_measures', 
        'user_input.py',
        )
    assert manager.user_input_module_file_path == file_path
    string = 'scoremanager.materialpackages.red_sargasso_measures.user_input'
    assert manager.user_input_module_package_path == string


def test_MaterialPackageManager_read_only_attributes_03():
    r'''Handmade material.
    '''

    string = 'scoremanager.materialpackages.red_notes'
    manager = scoremanager.managers.MaterialPackageManager(string)
    assert manager._breadcrumb == 'red notes'
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
        'red_notes', 
        'illustration_builder.py',
        )
    assert manager.illustration_builder_module_file_path == file_path
    string = 'scoremanager.materialpackages.red_notes.illustration_builder'
    assert manager.illustration_builder_package_path == string
    assert manager.illustration_builder_module_manager is not None
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'red_notes', 
        'illustration.ly',
        )
    assert manager.illustration_ly_file_path == file_path
    assert manager.illustration_ly_file_manager is not None
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'red_notes', 
        'illustration.pdf',
        )
    assert manager.illustration_pdf_file_path == file_path
    assert manager.illustration_pdf_file_manager is not None
    assert manager.is_handmade
    assert not manager.is_managermade
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'red_notes', 
        'material_definition.py',
        )
    assert manager.material_definition_module_file_path == file_path
    string = 'scoremanager.materialpackages.red_notes.material_definition'
    assert manager.material_definition_package_path == string
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'red_notes',
        )
    assert manager.material_package_directory == file_path
    assert manager.material_package_manager is None
    assert manager.material_package_manager_class_name is None
    assert manager.material_package_name == 'red_notes'
    assert manager.space_delimited_material_package_name == 'red notes'
    assert manager.material_package_name == 'red_notes'
    assert all(isinstance(x, Note) for x in manager.material_definition)
    assert manager.output_material_module_body_lines is not None
    file_path = os.path.join(
        manager._configuration.abjad_material_packages_directory_path, 
        'red_notes', 
        'output_material.py',
        )
    assert manager.output_material_module_file_path == file_path
    string = 'scoremanager.materialpackages.red_notes.output_material'
    assert manager.output_material_module_path == string
    assert manager.output_material_module_manager is not None
    assert manager.should_have_illustration
    assert manager.should_have_illustration_builder_module
    assert manager.should_have_illustration_ly
    assert manager.should_have_illustration_pdf
    assert manager.should_have_material_definition_module
    assert manager.should_have_output_material_module
    assert not  manager.should_have_user_input_module
    assert manager.user_input_module_file_path is None
    assert manager.user_input_module_package_path is None
