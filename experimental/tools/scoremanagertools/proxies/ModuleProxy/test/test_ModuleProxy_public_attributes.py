# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_ModuleProxy_public_attributes_01():
    r'''Without path.
    '''

    proxy = scoremanagertools.proxies.ModuleProxy()

    assert proxy._breadcrumb == 'module proxy'
    assert not proxy.exists()
    assert not proxy.read_lines()
    assert proxy._generic_class_name == 'module'
    assert proxy._space_delimited_lowercase_name is None
    assert not proxy.is_versioned()
    assert proxy.packagesystem_path is None
    assert proxy.packagesystem_basename is None
    assert proxy.parent_directory_filesystem_path is None
    assert proxy.parent_directory_filesystem_path is None
    assert proxy.parent_directory_packagesystem_path is None
    assert proxy.filesystem_path is None
    assert proxy._plural_generic_class_name == 'modules'
    assert proxy.filesystem_basename is None
    assert proxy._svn_add_command is None
    assert proxy._temporary_asset_name == 'temporary_module.py'


def test_ModuleProxy_public_attributes_02():
    r'''With path.
    '''

    configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    packagesystem_path = '.'.join([
        configuration.built_in_material_packages_package_path, 'red_notes', 'material_definition'])
    proxy = scoremanagertools.proxies.ModuleProxy(packagesystem_path=packagesystem_path)

    assert proxy._breadcrumb == 'material_definition.py'
    assert proxy.exists()
    assert proxy.read_lines()
    assert proxy._generic_class_name == 'module'
    assert proxy._space_delimited_lowercase_name == 'material definition'
    assert proxy.is_versioned()
    assert proxy.packagesystem_path == packagesystem_path
    assert proxy.packagesystem_basename == 'material_definition'
    assert proxy.parent_directory_filesystem_path == os.path.join(
        proxy.configuration.built_in_material_packages_directory_path, 'red_notes')
    assert proxy.parent_directory_filesystem_path == os.path.join(
        proxy.configuration.built_in_material_packages_directory_path, 'red_notes')
    assert proxy.parent_directory_packagesystem_path == '.'.join([
        proxy.configuration.built_in_material_packages_package_path, 'red_notes'])
    assert proxy.filesystem_path == os.path.join(
        proxy.configuration.built_in_material_packages_directory_path, 'red_notes', 'material_definition.py')
    assert proxy._plural_generic_class_name == 'modules'
    assert proxy.filesystem_basename == 'material_definition.py'
    assert proxy._svn_add_command
    assert proxy._temporary_asset_name == 'temporary_module.py'
