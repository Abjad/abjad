# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_ModuleManager_public_attributes_01():
    r'''Without path.
    '''

    manager = scoremanagertools.managers.ModuleManager()

    assert manager._breadcrumb == 'module manager'
    assert not manager.read_lines()
    assert manager._get_space_delimited_lowercase_name() is None
    assert not manager.is_versioned()
    assert manager.packagesystem_path is None
    assert manager.filesystem_path is None
    assert manager._repository_add_command is None


def test_ModuleManager_public_attributes_02():
    r'''With path.
    '''

    configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    packagesystem_path = '.'.join([
        configuration.built_in_material_packages_package_path, 'red_notes', 'material_definition'])
    manager = scoremanagertools.managers.ModuleManager(packagesystem_path=packagesystem_path)

    assert manager._breadcrumb == 'material_definition.py'
    assert manager.read_lines()
    assert manager._get_space_delimited_lowercase_name() == 'material definition'
    assert manager.is_versioned()
    assert manager.packagesystem_path == packagesystem_path
    assert manager.filesystem_path == os.path.join(
        manager.configuration.built_in_material_packages_directory_path, 'red_notes', 'material_definition.py')
    assert manager._repository_add_command
