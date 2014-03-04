# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler__make_data_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materials.testnumbers'
    assert not wrangler._configuration.package_exists(string)
    path = os.path.join(
        wrangler._configuration.abjad_material_packages_directory_path,
        'testnumbers',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'material_definition.py', 
        ]

    try:
        wrangler._make_data_package(path)
        assert wrangler._configuration.package_exists(string)
        manager = scoremanager.managers.MaterialManager(path)
        assert manager._list_directory() == directory_entries
        assert manager._interpret_material_definition_module() is None
        output_material = manager._execute_output_material_module()
        assert output_material is None
    finally:
        manager._remove()
        assert not wrangler._configuration.package_exists(string)


def test_MaterialPackageWrangler__make_data_package_02():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materials.example_numbers'
    assert wrangler._configuration.package_exists(string)
    statement = "wrangler._make_data_package("
    statement += "'scoremanager.materials.example_numbers')"
    assert pytest.raises(Exception, statement)


def test_MaterialPackageWrangler__make_data_package_03():
    r'''With custom metadata.
    '''

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materials.testnumbers'
    assert not wrangler._configuration.package_exists(string)
    path = os.path.join(
        wrangler._configuration.abjad_material_packages_directory_path,
        'testnumbers',
        )

    try:
        metadata = {'color': 'red', 'is_colored': True}
        wrangler._make_data_package(path, metadata=metadata)
        assert wrangler._configuration.package_exists(string)
        manager = scoremanager.managers.MaterialManager(path)
        assert manager._get_metadatum('color') == 'red'
        assert manager._get_metadatum('is_colored')
    finally:
        manager._remove()
        assert not wrangler._configuration.package_exists(string)
