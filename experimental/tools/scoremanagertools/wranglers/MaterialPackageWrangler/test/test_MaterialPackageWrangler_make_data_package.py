# -*- encoding: utf-8 -*-
import py
from experimental import *


def test_MaterialPackageWrangler_make_data_package_01():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnumbers')

    try:
        wrangler.make_data_package('experimental.tools.scoremanagertools.materialpackages.testnumbers')
        assert wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnumbers')
        mpp = scoremanagertools.proxies.MaterialPackageManager('experimental.tools.scoremanagertools.materialpackages.testnumbers')
        assert mpp.is_data_only
        assert mpp.list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnumbers')


def test_MaterialPackageWrangler_make_data_package_02():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.red_numbers')
    assert py.test.raises(Exception, "wrangler.make_data_package('experimental.tools.scoremanagertools.materialpackages.red_numbers')")


def test_MaterialPackageWrangler_make_data_package_03():
    r'''Interactively.
    '''

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnumbers')

    try:
        wrangler.interactively_make_data_package(pending_user_input='testnumbers q')
        assert wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnumbers')
        mpp = scoremanagertools.proxies.MaterialPackageManager('experimental.tools.scoremanagertools.materialpackages.testnumbers')
        assert mpp.is_data_only
        assert mpp.list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnumbers')


def test_MaterialPackageWrangler_make_data_package_04():
    r'''With custom tags.
    '''

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnumbers')

    try:
        tags = {'color': 'red', 'is_colored': True}
        wrangler.make_data_package('experimental.tools.scoremanagertools.materialpackages.testnumbers', tags=tags)
        assert wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnumbers')
        mpp = scoremanagertools.proxies.MaterialPackageManager('experimental.tools.scoremanagertools.materialpackages.testnumbers')
        assert mpp.get_metadata('color') == 'red'
        assert mpp.get_metadata('is_colored')
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnumbers')
