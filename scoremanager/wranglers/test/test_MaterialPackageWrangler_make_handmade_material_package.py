# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_make_handmade_material_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.testnotes'
    assert not wrangler.configuration.packagesystem_path_exists(string)


    try:
        wrangler.make_handmade_material_package(string)
        assert wrangler.configuration.packagesystem_path_exists(string)
        mpp = scoremanager.managers.MaterialPackageManager(string)
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists(string)


def test_MaterialPackageWrangler_make_handmade_material_package_02():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.red_notes'
    assert wrangler.configuration.packagesystem_path_exists(string)
    statement = 'wrangler.make_handmade_material_package'
    statement += "('scoremanager.materialpackages.red_notes')"
    assert pytest.raises(Exception, statement)


def test_MaterialPackageWrangler_make_handmade_material_package_03():
    r'''Interactively.
    '''

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.testnotes'
    assert not wrangler.configuration.packagesystem_path_exists(string)

    try:
        wrangler.interactively_make_handmade_material_package(
            pending_user_input='testnotes q')
        assert wrangler.configuration.packagesystem_path_exists(string)
        mpp = scoremanager.managers.MaterialPackageManager(string)
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists(string)


def test_MaterialPackageWrangler_make_handmade_material_package_04():
    r'''With custom tags.
    '''

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.testnotes'
    assert not wrangler.configuration.packagesystem_path_exists(string)

    try:
        tags = {'color': 'red', 'is_colored': True}
        wrangler.make_handmade_material_package(string, tags=tags)
        assert wrangler.configuration.packagesystem_path_exists(string)
        mpp = scoremanager.managers.MaterialPackageManager(string)
        assert mpp._get_metadata('color') == 'red'
        assert mpp._get_metadata('is_colored')
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists(string)
