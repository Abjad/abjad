# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_make_numeric_sequence_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.testsequence'
    assert not wrangler.configuration.packagesystem_path_exists(string)

    try:
        wrangler.make_numeric_sequence_package(string)
        assert wrangler.configuration.packagesystem_path_exists(string)
        mpp = scoremanager.managers.MaterialPackageManager(string)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert mpp._get_metadatum('is_numeric_sequence')
        assert mpp._get_metadatum('is_material_package')
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists(string)


def test_MaterialPackageWrangler_make_numeric_sequence_package_02():
    r'''Interactively.
    '''

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.testsequence'
    assert not wrangler.configuration.packagesystem_path_exists(string)

    try:
        wrangler.interactively_make_numeric_sequence_package(
            pending_user_input='testsequence')
        assert wrangler.configuration.packagesystem_path_exists(string)
        mpp = scoremanager.managers.MaterialPackageManager(string)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert mpp._get_metadatum('is_numeric_sequence')
        assert mpp._get_metadatum('is_material_package')
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists(string)
