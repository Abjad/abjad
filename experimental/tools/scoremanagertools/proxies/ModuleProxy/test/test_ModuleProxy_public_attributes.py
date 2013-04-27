import os
import py
from experimental import *


def test_ModuleProxy_public_attributes_01():
    '''Without path.
    '''

    proxy = scoremanagertools.proxies.ModuleProxy()

    assert proxy.breadcrumb == 'module proxy'
    assert not proxy.exists
    assert not proxy.file_lines
    assert proxy.generic_class_name == 'module'
    assert proxy.grandparent_directory_path is None
    assert proxy.grandparent_package_path is None
    assert proxy.human_readable_name is None
    assert not proxy.is_versioned
    assert proxy.module_path is None
    assert proxy.module_name is None
    assert proxy.parent_directory_path is None
    assert proxy.parent_directory_path is None
    assert proxy.parent_package_path is None
    assert proxy.parent_package_initializer_file_name is None
    assert proxy.path is None
    assert proxy.plural_generic_class_name == 'modules'
    assert proxy.name is None
    assert proxy.name_without_extension is None
    assert proxy.svn_add_command is None
    assert proxy.temporary_asset_name == 'temporary_module.py'


def test_ModuleProxy_public_attributes_02():
    '''With path.
    '''

    score_manager_object = scoremanagertools.core.ScoreManagerObject()
    module_path = '.'.join([
        score_manager_object.configuration.score_external_materials_package_path, 'red_notes', 'material_definition'])
    proxy = scoremanagertools.proxies.ModuleProxy(module_path=module_path)

    assert proxy.breadcrumb == 'material_definition.py'
    assert proxy.exists
    assert proxy.file_lines
    assert proxy.generic_class_name == 'module'
    assert proxy.grandparent_directory_path == proxy.configuration.SCORE_EXTERNAL_MATERIALS_DIRECTORY_PATH
    assert proxy.grandparent_package_path == proxy.configuration.score_external_materials_package_path
    assert proxy.human_readable_name == 'material definition'
    assert proxy.is_versioned
    assert proxy.module_path == module_path
    assert proxy.module_name == 'material_definition'
    assert proxy.parent_directory_path == os.path.join(
        proxy.configuration.SCORE_EXTERNAL_MATERIALS_DIRECTORY_PATH, 'red_notes')
    assert proxy.parent_directory_path == os.path.join(
        proxy.configuration.SCORE_EXTERNAL_MATERIALS_DIRECTORY_PATH, 'red_notes')
    assert proxy.parent_package_path == '.'.join([
        proxy.configuration.score_external_materials_package_path, 'red_notes'])
    assert proxy.parent_package_initializer_file_name == os.path.join(
        proxy.configuration.SCORE_EXTERNAL_MATERIALS_DIRECTORY_PATH, 'red_notes', '__init__.py')
    assert proxy.path == os.path.join(
        proxy.configuration.SCORE_EXTERNAL_MATERIALS_DIRECTORY_PATH, 'red_notes', 'material_definition.py')
    assert proxy.plural_generic_class_name == 'modules'
    assert proxy.name == 'material_definition.py'
    assert proxy.name_without_extension == 'material_definition'
    assert proxy.svn_add_command
    assert proxy.temporary_asset_name == 'temporary_module.py'
