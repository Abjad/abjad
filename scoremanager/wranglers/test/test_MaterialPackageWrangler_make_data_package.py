# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_make_data_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.testnumbers'
    assert not wrangler.configuration.package_exists(string)

    try:
        wrangler._make_data_package(string)
        assert wrangler.configuration.package_exists(string)
        manager = scoremanager.managers.MaterialPackageManager(string)
        assert manager._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not manager.has_output_material_module
        assert manager.material_definition is None
        assert manager.output_material is None
    finally:
        manager._remove()
        assert not wrangler.configuration.package_exists(string)


def test_MaterialPackageWrangler_make_data_package_02():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.red_numbers'
    assert wrangler.configuration.package_exists(string)
    statement = "wrangler._make_data_package('scoremanager.materialpackages.red_numbers')"
    assert pytest.raises(Exception, statement)


def test_MaterialPackageWrangler_make_data_package_03():
    r'''Interactively.
    '''

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.testnumbers'
    assert not wrangler.configuration.package_exists(string)

    try:
        wrangler.make_data_package(pending_user_input='testnumbers q')
        assert wrangler.configuration.package_exists(string)
        manager = scoremanager.managers.MaterialPackageManager(string)
        assert manager._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
    finally:
        manager._remove()
        assert not wrangler.configuration.package_exists(string)


def test_MaterialPackageWrangler_make_data_package_04():
    r'''With custom metadata.
    '''

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.testnumbers'
    assert not wrangler.configuration.package_exists(string)

    try:
        metadata = {'color': 'red', 'is_colored': True}
        wrangler._make_data_package(string, metadata=metadata)
        assert wrangler.configuration.package_exists(string)
        manager = scoremanager.managers.MaterialPackageManager(string)
        assert manager._get_metadatum('color') == 'red'
        assert manager._get_metadatum('is_colored')
    finally:
        manager._remove()
        assert not wrangler.configuration.package_exists(string)
