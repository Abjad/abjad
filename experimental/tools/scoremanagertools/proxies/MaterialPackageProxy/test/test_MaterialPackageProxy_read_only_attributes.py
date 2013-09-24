# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_MaterialPackageProxy_read_only_attributes_01():
    r'''Data-only package.
    '''

    mpp = scoremanagertools.proxies.MaterialPackageProxy(
        'experimental.tools.scoremanagertools.materialpackages.red_numbers')
    assert     mpp._breadcrumb == 'red numbers'
    assert not mpp.has_illustration_builder_module
    assert not mpp.has_illustration_ly
    assert not mpp.has_illustration_pdf
    assert     mpp.has_material_definition
    assert     mpp.has_material_definition_module
    assert not mpp.has_material_package_maker
    assert     mpp.has_output_material
    assert     mpp.has_output_material_module
    assert not mpp.has_user_input_module
    assert not mpp.has_user_input_wrapper_on_disk
    assert     mpp.illustration_builder_module_file_name is None
    assert     mpp.illustration_builder_packagesystem_path is None
    assert     mpp.illustration_ly_file_name is None
    assert     mpp.illustration_pdf_file_name is None
    # TODO:
    #assert not mpp.is_changed
    assert     mpp.is_data_only
    assert     mpp.is_handmade
    assert     mpp.material_definition == [1, 2, 3, 4, 5]
    assert     mpp.material_definition_module_file_name == \
        os.path.join(mpp.configuration.built_in_material_packages_directory_path, 'red_numbers', 'material_definition.py')
    assert     mpp.material_definition_packagesystem_path == \
        'experimental.tools.scoremanagertools.materialpackages.red_numbers.material_definition'
    assert     mpp.material_definition_module_proxy is not None
    assert     mpp.material_package_directory == \
        os.path.join(mpp.configuration.built_in_material_packages_directory_path, 'red_numbers')
    assert     mpp.material_package_maker is None
    assert     mpp.material_package_maker_class_name is None
    assert     mpp.material_package_name == 'red_numbers'
    assert     mpp.space_delimited_material_package_name == 'red numbers'
    assert     mpp.material_package_name == 'red_numbers'
    assert     mpp.output_material_module_body_lines == ['red_numbers = [1, 2, 3, 4, 5]']
    assert     mpp.output_material_module_file_name == \
        os.path.join(mpp.configuration.built_in_material_packages_directory_path, 'red_numbers', 'output_material.py')
    assert     mpp.output_material_module_path == \
        'experimental.tools.scoremanagertools.materialpackages.red_numbers.output_material'
    assert      mpp.output_material_module_proxy is not None
    assert not  mpp.should_have_illustration
    assert not  mpp.should_have_illustration_builder_module
    assert not  mpp.should_have_illustration_ly
    assert not  mpp.should_have_illustration_pdf
    assert      mpp.should_have_material_definition_module
    assert      mpp.should_have_output_material_module
    assert not  mpp.should_have_user_input_module
    assert      mpp.stylesheet_file_name_on_disk is None
    assert      mpp.user_input_module_file_name is None
    assert      mpp.user_input_module_packagesystem_path is None
    assert      mpp.user_input_module_proxy is None


def test_MaterialPackageProxy_read_only_attributes_02():
    r'''Makermade material.
    '''

    mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker(
        'experimental.tools.scoremanagertools.materialpackages.red_sargasso_measures')
    assert     mpp._breadcrumb == 'red sargasso measures'
    assert not mpp.has_illustration_builder_module
    assert     mpp.has_illustration_ly
    assert     mpp.has_illustration_pdf
    assert not mpp.has_material_definition
    assert not mpp.has_material_definition_module
    assert     mpp.has_material_package_maker
    assert     mpp.has_output_material
    assert     mpp.has_output_material_module
    assert     mpp.has_user_input_module
    assert     mpp.has_user_input_wrapper_on_disk
    assert     mpp.has_user_input_wrapper_in_memory
    assert     mpp.illustration_builder_module_file_name is None
    assert     mpp.illustration_builder_packagesystem_path is None
    assert     mpp.illustration_ly_file_name == \
        os.path.join(mpp.configuration.built_in_material_packages_directory_path, 'red_sargasso_measures', 'illustration.ly')
    assert     mpp.illustration_ly_file_proxy is not None
    assert     mpp.illustration_pdf_file_name == \
        os.path.join(mpp.configuration.built_in_material_packages_directory_path, 'red_sargasso_measures', 'illustration.pdf')
    # TODO:
    #assert not mpp.is_changed
    assert not mpp.is_data_only
    assert not mpp.is_handmade
    assert     mpp.is_makermade
    assert     mpp.material_definition_module_file_name is None
    assert     mpp.material_definition_packagesystem_path is None
    assert     mpp.material_definition_module_proxy is None
    assert     mpp.material_package_directory == \
        os.path.join(mpp.configuration.built_in_material_packages_directory_path, 'red_sargasso_measures')
    assert     mpp.material_package_maker is scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker
    assert     mpp.material_package_maker_class_name == 'SargassoMeasureMaterialPackageMaker'
    assert     mpp.material_package_name == 'red_sargasso_measures'
    assert     mpp.space_delimited_material_package_name == 'red sargasso measures'
    assert     mpp.material_package_name == 'red_sargasso_measures'
    assert     mpp.output_material_module_body_lines is None
    assert     mpp.output_material_module_file_name == \
        os.path.join(mpp.configuration.built_in_material_packages_directory_path, 'red_sargasso_measures', 'output_material.py')
    assert     mpp.output_material_module_path == \
        'experimental.tools.scoremanagertools.materialpackages.red_sargasso_measures.output_material'
    assert      mpp.output_material_module_proxy is not None
    assert      mpp.should_have_illustration
    assert not  mpp.should_have_illustration_builder_module
    assert      mpp.should_have_illustration_ly
    assert      mpp.should_have_illustration_pdf
    assert not  mpp.should_have_material_definition_module
    assert      mpp.should_have_output_material_module
    assert      mpp.should_have_user_input_module
    # TODO:
    #assert      mpp.stylesheet_file_name_on_disk is None
    #assert      mpp.stylesheet_file_proxy is None
    assert      mpp.user_input_module_file_name == \
        os.path.join(mpp.configuration.built_in_material_packages_directory_path, 'red_sargasso_measures', 'user_input.py')
    assert      mpp.user_input_module_packagesystem_path == \
        'experimental.tools.scoremanagertools.materialpackages.red_sargasso_measures.user_input'
    assert      mpp.user_input_module_proxy is not None


def test_MaterialPackageProxy_read_only_attributes_03():
    r'''Handmade material.
    '''

    mpp = scoremanagertools.proxies.MaterialPackageProxy(
        'experimental.tools.scoremanagertools.materialpackages.red_notes')
    assert     mpp._breadcrumb == 'red notes'
    assert     mpp.has_illustration_builder_module
    assert     mpp.has_illustration_ly
    assert     mpp.has_illustration_pdf
    assert     mpp.has_material_definition
    assert     mpp.has_material_definition_module
    assert not mpp.has_material_package_maker
    assert     mpp.has_output_material
    assert     mpp.has_output_material_module
    assert not mpp.has_user_input_module
    assert not mpp.has_user_input_wrapper_on_disk
    # TODO: make this work again ... or remove import-needy property altogether
    #assert     mpp.illustration is not None
    assert     mpp.illustration_builder_module_file_name == \
        os.path.join(mpp.configuration.built_in_material_packages_directory_path, 'red_notes', 'illustration_builder.py')
    assert     mpp.illustration_builder_packagesystem_path == \
        'experimental.tools.scoremanagertools.materialpackages.red_notes.illustration_builder'
    assert     mpp.illustration_builder_module_proxy is not None
    assert     mpp.illustration_ly_file_name == \
        os.path.join(mpp.configuration.built_in_material_packages_directory_path, 'red_notes', 'illustration.ly')
    assert     mpp.illustration_ly_file_proxy is not None
    assert     mpp.illustration_pdf_file_name == \
        os.path.join(mpp.configuration.built_in_material_packages_directory_path, 'red_notes', 'illustration.pdf')
    assert     mpp.illustration_pdf_file_proxy is not None
    # TODO:
    #assert not mpp.is_changed
    assert not mpp.is_data_only
    assert     mpp.is_handmade
    assert not mpp.is_makermade
    assert     mpp.material_definition_module_file_name == \
        os.path.join(mpp.configuration.built_in_material_packages_directory_path, 'red_notes', 'material_definition.py')
    assert     mpp.material_definition_packagesystem_path == \
        'experimental.tools.scoremanagertools.materialpackages.red_notes.material_definition'
    assert     mpp.material_definition_module_proxy is not None
    assert     mpp.material_package_directory == \
        os.path.join(mpp.configuration.built_in_material_packages_directory_path, 'red_notes')
    assert     mpp.material_package_maker is None
    assert     mpp.material_package_maker_class_name is None
    assert     mpp.material_package_name == 'red_notes'
    assert     mpp.space_delimited_material_package_name == 'red notes'
    assert     mpp.material_package_name == 'red_notes'
    assert     all(isinstance(x, Note) for x in mpp.material_definition)
    assert     mpp.output_material_module_body_lines is not None
    assert     mpp.output_material_module_file_name == \
        os.path.join(mpp.configuration.built_in_material_packages_directory_path, 'red_notes', 'output_material.py')
    assert     mpp.output_material_module_path == \
        'experimental.tools.scoremanagertools.materialpackages.red_notes.output_material'
    assert      mpp.output_material_module_proxy is not None
    assert      mpp.should_have_illustration
    assert      mpp.should_have_illustration_builder_module
    assert      mpp.should_have_illustration_ly
    assert      mpp.should_have_illustration_pdf
    assert      mpp.should_have_material_definition_module
    assert      mpp.should_have_output_material_module
    assert not  mpp.should_have_user_input_module
    assert      mpp.user_input_module_file_name is None
    assert      mpp.user_input_module_packagesystem_path is None
    assert      mpp.user_input_module_proxy is None
