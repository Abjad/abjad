import os
import scf
from abjad.tools import measuretools
from abjad.tools import notetools


def test_MaterialPackageProxy_read_only_attributes_01():
    '''Data-only package.
    '''

    mpp = scf.proxies.MaterialPackageProxy('materials.red_numbers')
    assert     mpp.breadcrumb == 'red numbers'
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
    assert     mpp.illustration is None
    assert     mpp.illustration_builder_module_file_name is None
    assert     mpp.illustration_builder_module_importable_name is None
    assert     mpp.illustration_builder_module_proxy is None
    assert     mpp.illustration_ly_file_name is None
    assert     mpp.illustration_ly_file_proxy is None
    assert     mpp.illustration_pdf_file_name is None
    assert     mpp.illustration_pdf_file_proxy is None
    # TODO:
    #assert not mpp.is_changed
    assert     mpp.is_data_only
    assert     mpp.is_handmade
    assert     mpp.material_definition == [1, 2, 3, 4, 5]
    assert     mpp.material_definition_module_file_name == \
        os.path.join(os.environ.get('SCFMATERIALSPATH'), 'red_numbers', 'material_definition.py')
    assert     mpp.material_definition_module_importable_name == \
        'materials.red_numbers.material_definition'
    assert     mpp.material_definition_module_proxy is not None
    assert     mpp.material_package_directory == \
        os.path.join(os.environ.get('SCFMATERIALSPATH'), 'red_numbers')
    assert     mpp.material_package_maker is None
    assert     mpp.material_package_maker_class_name is None
    assert     mpp.material_package_short_name == 'red_numbers'
    assert     mpp.material_spaced_name == 'red numbers'
    assert     mpp.material_underscored_name == 'red_numbers'
    assert     mpp.output_material == [1, 2, 3, 4, 5]
    assert     mpp.output_material_module_body_lines == ['red_numbers = [1, 2, 3, 4, 5]']
    assert     mpp.output_material_module_file_name == \
        os.path.join(os.environ.get('SCFMATERIALSPATH'), 'red_numbers', 'output_material.py')
    assert     mpp.output_material_module_importable_name == \
        'materials.red_numbers.output_material'
    assert      mpp.output_material_module_proxy is not None
    assert not  mpp.should_have_illustration
    assert not  mpp.should_have_illustration_builder_module
    assert not  mpp.should_have_illustration_ly
    assert not  mpp.should_have_illustration_pdf
    assert      mpp.should_have_material_definition_module
    assert      mpp.should_have_output_material_module
    assert not  mpp.should_have_user_input_module
    assert      mpp.stylesheet_file_name_on_disk is None
    assert      mpp.stylesheet_file_proxy is None
    assert      mpp.user_input_module_file_name is None
    assert      mpp.user_input_module_importable_name is None
    assert      mpp.user_input_module_proxy is None


def test_MaterialPackageProxy_read_only_attributes_02():
    '''Makermade material.
    '''

    mpp = scf.makers.SargassoMeasureMaterialPackageMaker('materials.red_sargasso_measures')
    assert     mpp.breadcrumb == 'red sargasso measures'
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
    assert     mpp.illustration is not None
    assert     mpp.illustration_builder_module_file_name is None
    assert     mpp.illustration_builder_module_importable_name is None
    assert     mpp.illustration_builder_module_proxy is None
    assert     mpp.illustration_ly_file_name == \
        os.path.join(os.environ.get('SCFMATERIALSPATH'), 'red_sargasso_measures', 'illustration.ly')
    assert     mpp.illustration_ly_file_proxy is not None
    assert     mpp.illustration_pdf_file_name == \
        os.path.join(os.environ.get('SCFMATERIALSPATH'), 'red_sargasso_measures', 'illustration.pdf')
    assert     mpp.illustration_pdf_file_proxy is not None
    # TODO:
    #assert not mpp.is_changed
    assert not mpp.is_data_only
    assert not mpp.is_handmade
    assert     mpp.is_makermade
    assert     mpp.material_definition_module_file_name is None
    assert     mpp.material_definition_module_importable_name is None
    assert     mpp.material_definition_module_proxy is None
    assert     mpp.material_package_directory == \
        os.path.join(os.environ.get('SCFMATERIALSPATH'), 'red_sargasso_measures')
    assert     mpp.material_package_maker is scf.makers.SargassoMeasureMaterialPackageMaker
    assert     mpp.material_package_maker_class_name == 'SargassoMeasureMaterialPackageMaker'
    assert     mpp.material_package_short_name == 'red_sargasso_measures'
    assert     mpp.material_spaced_name == 'red sargasso measures'
    assert     mpp.material_underscored_name == 'red_sargasso_measures'
    assert     measuretools.all_are_measures(mpp.output_material)
    assert     mpp.output_material_module_body_lines is None
    assert     mpp.output_material_module_file_name == \
        os.path.join(os.environ.get('SCFMATERIALSPATH'), 'red_sargasso_measures', 'output_material.py')
    assert     mpp.output_material_module_importable_name == \
        'materials.red_sargasso_measures.output_material'
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
        os.path.join(os.environ.get('SCFMATERIALSPATH'), 'red_sargasso_measures', 'user_input.py')
    assert      mpp.user_input_module_importable_name == \
        'materials.red_sargasso_measures.user_input'
    assert      mpp.user_input_module_proxy is not None


def test_MaterialPackageProxy_read_only_attributes_03():
    '''Handmade material.
    '''

    mpp = scf.proxies.MaterialPackageProxy('materials.red_notes')
    assert     mpp.breadcrumb == 'red notes'
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
    assert     mpp.illustration is not None
    assert     mpp.illustration_builder_module_file_name == \
        os.path.join(os.environ.get('SCFMATERIALSPATH'), 'red_notes', 'illustration_builder.py')
    assert     mpp.illustration_builder_module_importable_name == \
        'materials.red_notes.illustration_builder'
    assert     mpp.illustration_builder_module_proxy is not None
    assert     mpp.illustration_ly_file_name == \
        os.path.join(os.environ.get('SCFMATERIALSPATH'), 'red_notes', 'illustration.ly')
    assert     mpp.illustration_ly_file_proxy is not None
    assert     mpp.illustration_pdf_file_name == \
        os.path.join(os.environ.get('SCFMATERIALSPATH'), 'red_notes', 'illustration.pdf')
    assert     mpp.illustration_pdf_file_proxy is not None
    # TODO:
    #assert not mpp.is_changed
    assert not mpp.is_data_only
    assert     mpp.is_handmade
    assert not mpp.is_makermade
    assert     mpp.material_definition_module_file_name == \
        os.path.join(os.environ.get('SCFMATERIALSPATH'), 'red_notes', 'material_definition.py')
    assert     mpp.material_definition_module_importable_name == \
        'materials.red_notes.material_definition'
    assert     mpp.material_definition_module_proxy is not None
    assert     mpp.material_package_directory == \
        os.path.join(os.environ.get('SCFMATERIALSPATH'), 'red_notes')
    assert     mpp.material_package_maker is None
    assert     mpp.material_package_maker_class_name is None
    assert     mpp.material_package_short_name == 'red_notes'
    assert     mpp.material_spaced_name == 'red notes'
    assert     mpp.material_underscored_name == 'red_notes'
    assert     notetools.all_are_notes(mpp.material_definition)
    assert     mpp.output_material_module_body_lines is not None
    assert     mpp.output_material_module_file_name == \
        os.path.join(os.environ.get('SCFMATERIALSPATH'), 'red_notes', 'output_material.py')
    assert     mpp.output_material_module_importable_name == \
        'materials.red_notes.output_material'
    assert      mpp.output_material_module_proxy is not None
    assert      mpp.should_have_illustration
    assert      mpp.should_have_illustration_builder_module
    assert      mpp.should_have_illustration_ly
    assert      mpp.should_have_illustration_pdf
    assert      mpp.should_have_material_definition_module
    assert      mpp.should_have_output_material_module
    assert not  mpp.should_have_user_input_module
    assert      mpp.stylesheet_file_name_on_disk == \
        os.path.join(os.environ.get('SCFPATH'), 'stylesheets', 'clean_letter_14.ly')
    # TODO:
    #assert      mpp.stylesheet_file_proxy is not None
    assert      mpp.user_input_module_file_name is None
    assert      mpp.user_input_module_importable_name is None
    assert      mpp.user_input_module_proxy is None
