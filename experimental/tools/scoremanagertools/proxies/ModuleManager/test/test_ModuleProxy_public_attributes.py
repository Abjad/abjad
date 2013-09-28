# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_ModuleManager_public_attributes_01():
    r'''Without path.
    '''

    proxy = scoremanagertools.proxies.ModuleManager()

    assert proxy._breadcrumb == 'module manager'
    assert not proxy.read_lines()
    assert proxy._get_space_delimited_lowercase_name() is None
    assert not proxy.is_versioned()
    assert proxy.packagesystem_path is None
    assert proxy.filesystem_path is None
    assert proxy.filesystem_basename is None
    assert proxy._repository_add_command is None


def test_ModuleManager_public_attributes_02():
    r'''With path.
    '''

    configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    packagesystem_path = '.'.join([
        configuration.built_in_material_packages_package_path, 'red_notes', 'material_definition'])
    proxy = scoremanagertools.proxies.ModuleManager(packagesystem_path=packagesystem_path)

    assert proxy._breadcrumb == 'material_definition.py'
    assert proxy.read_lines()
    assert proxy._get_space_delimited_lowercase_name() == 'material definition'
    assert proxy.is_versioned()
    assert proxy.packagesystem_path == packagesystem_path
    assert proxy.filesystem_path == os.path.join(
        proxy.configuration.built_in_material_packages_directory_path, 'red_notes', 'material_definition.py')
    assert proxy.filesystem_basename == 'material_definition.py'
    assert proxy._repository_add_command
