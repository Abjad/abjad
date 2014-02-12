# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_make_numeric_sequence_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists('scoremanager.materialpackages.testsequence')

    try:
        wrangler.make_numeric_sequence_package('scoremanager.materialpackages.testsequence')
        assert wrangler.configuration.packagesystem_path_exists('scoremanager.materialpackages.testsequence')
        mpp = scoremanager.managers.MaterialPackageManager('scoremanager.materialpackages.testsequence')
        assert mpp.is_data_only
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert mpp._get_metadata('is_numeric_sequence')
        assert mpp._get_metadata('is_material_package')
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists('scoremanager.materialpackages.testsequence')


def test_MaterialPackageWrangler_make_numeric_sequence_package_02():
    r'''Interactively.
    '''

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists('scoremanager.materialpackages.testsequence')

    try:
        wrangler.interactively_make_numeric_sequence_package(pending_user_input='testsequence')
        assert wrangler.configuration.packagesystem_path_exists('scoremanager.materialpackages.testsequence')
        mpp = scoremanager.managers.MaterialPackageManager('scoremanager.materialpackages.testsequence')
        assert mpp.is_data_only
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert mpp._get_metadata('is_numeric_sequence')
        assert mpp._get_metadata('is_material_package')
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists('scoremanager.materialpackages.testsequence')
