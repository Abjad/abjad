import os
import py
from experimental import *


def test_ModuleProxy_public_attributes_01():
    '''Without path.
    '''

    proxy = scoremanagertools.proxies.ModuleProxy()

    assert proxy._breadcrumb == 'module proxy'
    assert not proxy.exists()
    assert not proxy.read_lines()
    assert proxy._generic_class_name == 'module'
    assert proxy.grandparent_directory_path is None
    assert proxy.grandparent_package_path is None
    assert proxy._space_delimited_lowercase_name is None
    assert not proxy.is_versioned()
    assert proxy.module_path is None
    assert proxy.module_name is None
    assert proxy.filesystem_directory_name is None
    assert proxy.filesystem_directory_name is None
    assert proxy.parent_package_path is None
    assert proxy.parent_package_initializer_file_name is None
    assert proxy.filesystem_path is None
    assert proxy._plural_generic_class_name == 'modules'
    assert proxy.filesystem_basename is None
    assert proxy._svn_add_command is None
    assert proxy._temporary_asset_name == 'temporary_module.py'


def test_ModuleProxy_public_attributes_02():
    '''With path.
    '''

    configuration = scoremanagertools.core.ScoreManagerConfiguration()
    module_path = '.'.join([
        configuration.built_in_materials_package_path, 'red_notes', 'material_definition'])
    proxy = scoremanagertools.proxies.ModuleProxy(module_path=module_path)

    assert proxy._breadcrumb == 'material_definition.py'
    assert proxy.exists()
    assert proxy.read_lines()
    assert proxy._generic_class_name == 'module'
    assert proxy.grandparent_directory_path == proxy.configuration.built_in_materials_directory_path
    assert proxy.grandparent_package_path == proxy.configuration.built_in_materials_package_path
    assert proxy._space_delimited_lowercase_name == 'material definition'
    assert proxy.is_versioned()
    assert proxy.module_path == module_path
    assert proxy.module_name == 'material_definition'
    assert proxy.filesystem_directory_name == os.path.join(
        proxy.configuration.built_in_materials_directory_path, 'red_notes')
    assert proxy.filesystem_directory_name == os.path.join(
        proxy.configuration.built_in_materials_directory_path, 'red_notes')
    assert proxy.parent_package_path == '.'.join([
        proxy.configuration.built_in_materials_package_path, 'red_notes'])
    assert proxy.parent_package_initializer_file_name == os.path.join(
        proxy.configuration.built_in_materials_directory_path, 'red_notes', '__init__.py')
    assert proxy.filesystem_path == os.path.join(
        proxy.configuration.built_in_materials_directory_path, 'red_notes', 'material_definition.py')
    assert proxy._plural_generic_class_name == 'modules'
    assert proxy.filesystem_basename == 'material_definition.py'
    assert proxy._svn_add_command
    assert proxy._temporary_asset_name == 'temporary_module.py'
