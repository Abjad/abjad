# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_make_data_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.testnumbers'
    assert not wrangler.configuration.package_exists(string)

    try:
        wrangler.make_data_package(string)
        assert wrangler.configuration.package_exists(string)
        mpp = scoremanager.managers.MaterialPackageManager(string)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        mpp.remove()
        assert not wrangler.configuration.package_exists(string)


def test_MaterialPackageWrangler_make_data_package_02():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.red_numbers'
    assert wrangler.configuration.package_exists(string)
    statement = "wrangler.make_data_package('scoremanager.materialpackages.red_numbers')"
    assert pytest.raises(Exception, statement)


def test_MaterialPackageWrangler_make_data_package_03():
    r'''Interactively.
    '''

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.testnumbers'
    assert not wrangler.configuration.package_exists(string)

    try:
        wrangler.interactively_make_data_package(pending_user_input='testnumbers q')
        assert wrangler.configuration.package_exists(string)
        mpp = scoremanager.managers.MaterialPackageManager(string)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
    finally:
        mpp.remove()
        assert not wrangler.configuration.package_exists(string)


def test_MaterialPackageWrangler_make_data_package_04():
    r'''With custom metadata.
    '''

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.testnumbers'
    assert not wrangler.configuration.package_exists(string)

    try:
        metadata = {'color': 'red', 'is_colored': True}
        wrangler.make_data_package(string, metadata=metadata)
        assert wrangler.configuration.package_exists(string)
        mpp = scoremanager.managers.MaterialPackageManager(string)
        assert mpp._get_metadatum('color') == 'red'
        assert mpp._get_metadatum('is_colored')
    finally:
        mpp.remove()
        assert not wrangler.configuration.package_exists(string)
