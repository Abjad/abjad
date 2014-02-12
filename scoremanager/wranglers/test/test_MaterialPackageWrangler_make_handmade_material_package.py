# -*- encoding: utf-8 -*-
import pytest
from experimental import *


def test_MaterialPackageWrangler_make_handmade_material_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists(
        'scoremanager.materialpackages.testnotes')


    try:
        wrangler.make_handmade_material_package(
            'scoremanager.materialpackages.testnotes')
        assert wrangler.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnotes')
        mpp = scoremanager.managers.MaterialPackageManager(
            'scoremanager.materialpackages.testnotes')
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
        assert not wrangler.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnotes')


def test_MaterialPackageWrangler_make_handmade_material_package_02():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    assert wrangler.configuration.packagesystem_path_exists(
        'scoremanager.materialpackages.red_notes')
    assert pytest.raises(Exception, 'wrangler.make_handmade_material_package'
        "('scoremanager.materialpackages.red_notes')")


def test_MaterialPackageWrangler_make_handmade_material_package_03():
    r'''Interactively.
    '''

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists(
        'scoremanager.materialpackages.testnotes')


    try:
        wrangler.interactively_make_handmade_material_package(pending_user_input='testnotes q')
        assert wrangler.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnotes')
        mpp = scoremanager.managers.MaterialPackageManager(
            'scoremanager.materialpackages.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnotes')


def test_MaterialPackageWrangler_make_handmade_material_package_04():
    r'''With custom tags.
    '''

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists(
        'scoremanager.materialpackages.testnotes')


    try:
        tags = {'color': 'red', 'is_colored': True}
        wrangler.make_handmade_material_package(
            'scoremanager.materialpackages.testnotes', tags=tags)
        assert wrangler.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnotes')
        mpp = scoremanager.managers.MaterialPackageManager(
            'scoremanager.materialpackages.testnotes')
        assert mpp._get_metadata('color') == 'red'
        assert mpp._get_metadata('is_colored')
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnotes')
