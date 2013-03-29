import os
import py
import scf


def test_ModuleProxy_public_attributes_01():
    '''Without path.
    '''

    proxy = scf.proxies.ModuleProxy()

    assert proxy.breadcrumb == 'module proxy'
    assert not proxy.exists
    assert not proxy.file_lines
    assert proxy.generic_class_name == 'module'
    assert proxy.grandparent_package_directory_name is None
    assert proxy.grandparent_package_importable_name is None
    assert proxy.human_readable_name is None
    assert not proxy.is_versioned
    assert proxy.module_importable_name is None
    assert proxy.module_short_name is None
    assert proxy.parent_directory_name is None
    assert proxy.parent_package_directory_name is None
    assert proxy.parent_package_importable_name is None
    assert proxy.parent_package_initializer_file_name is None
    assert proxy.path_name is None
    assert proxy.plural_generic_class_name == 'modules'
    assert proxy.short_name is None
    assert proxy.short_name_without_extension is None
    assert proxy.svn_add_command is None
    assert proxy.temporary_asset_short_name == 'temporary_module.py'


def test_ModuleProxy_public_attributes_02():
    '''With path.
    '''

    scf_object = scf.core.SCFObject()
    module_importable_name = '.'.join([
        scf_object.score_external_materials_package_importable_name, 'red_notes', 'material_definition'])
    proxy = scf.proxies.ModuleProxy(module_importable_name=module_importable_name)

    assert proxy.breadcrumb == 'material_definition.py'
    assert proxy.exists
    assert proxy.file_lines
    assert proxy.generic_class_name == 'module'
    assert proxy.grandparent_package_directory_name == proxy.score_external_materials_package_path_name
    assert proxy.grandparent_package_importable_name == proxy.score_external_materials_package_importable_name
    assert proxy.human_readable_name == 'material definition'
    assert proxy.is_versioned
    assert proxy.module_importable_name == module_importable_name
    assert proxy.module_short_name == 'material_definition'
    assert proxy.parent_directory_name == os.path.join(
        proxy.score_external_materials_package_path_name, 'red_notes')
    assert proxy.parent_package_directory_name == os.path.join(
        proxy.score_external_materials_package_path_name, 'red_notes')
    assert proxy.parent_package_importable_name == '.'.join([
        proxy.score_external_materials_package_importable_name, 'red_notes'])
    assert proxy.parent_package_initializer_file_name == os.path.join(
        proxy.score_external_materials_package_path_name, 'red_notes', '__init__.py')
    assert proxy.path_name == os.path.join(
        proxy.score_external_materials_package_path_name, 'red_notes', 'material_definition.py')
    assert proxy.plural_generic_class_name == 'modules'
    assert proxy.short_name == 'material_definition.py'
    assert proxy.short_name_without_extension == 'material_definition'
    assert proxy.svn_add_command
    assert proxy.temporary_asset_short_name == 'temporary_module.py'
