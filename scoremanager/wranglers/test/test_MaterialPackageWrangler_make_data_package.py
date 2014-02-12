# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_make_data_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists('scoremanager.materialpackages.testnumbers')

    try:
        wrangler.make_data_package('scoremanager.materialpackages.testnumbers')
        assert wrangler.configuration.packagesystem_path_exists('scoremanager.materialpackages.testnumbers')
        mpp = scoremanager.managers.MaterialPackageManager('scoremanager.materialpackages.testnumbers')
        assert mpp.is_data_only
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
        assert not wrangler.configuration.packagesystem_path_exists('scoremanager.materialpackages.testnumbers')


def test_MaterialPackageWrangler_make_data_package_02():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    assert wrangler.configuration.packagesystem_path_exists('scoremanager.materialpackages.red_numbers')
    assert pytest.raises(Exception, "wrangler.make_data_package('scoremanager.materialpackages.red_numbers')")


def test_MaterialPackageWrangler_make_data_package_03():
    r'''Interactively.
    '''

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists('scoremanager.materialpackages.testnumbers')

    try:
        wrangler.interactively_make_data_package(pending_user_input='testnumbers q')
        assert wrangler.configuration.packagesystem_path_exists('scoremanager.materialpackages.testnumbers')
        mpp = scoremanager.managers.MaterialPackageManager('scoremanager.materialpackages.testnumbers')
        assert mpp.is_data_only
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists('scoremanager.materialpackages.testnumbers')


def test_MaterialPackageWrangler_make_data_package_04():
    r'''With custom tags.
    '''

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists('scoremanager.materialpackages.testnumbers')

    try:
        tags = {'color': 'red', 'is_colored': True}
        wrangler.make_data_package('scoremanager.materialpackages.testnumbers', tags=tags)
        assert wrangler.configuration.packagesystem_path_exists('scoremanager.materialpackages.testnumbers')
        mpp = scoremanager.managers.MaterialPackageManager('scoremanager.materialpackages.testnumbers')
        assert mpp._get_metadata('color') == 'red'
        assert mpp._get_metadata('is_colored')
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists('scoremanager.materialpackages.testnumbers')
