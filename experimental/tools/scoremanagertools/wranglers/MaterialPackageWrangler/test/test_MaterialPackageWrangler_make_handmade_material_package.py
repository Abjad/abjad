# -*- encoding: utf-8 -*-
import py
from experimental import *


def test_MaterialPackageWrangler_make_handmade_material_package_01():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists(
        'experimental.tools.scoremanagertools.materialpackages.testnotes')


    try:
        wrangler.make_handmade_material_package(
            'experimental.tools.scoremanagertools.materialpackages.testnotes')
        assert wrangler.configuration.packagesystem_path_exists(
            'experimental.tools.scoremanagertools.materialpackages.testnotes')
        mpp = scoremanagertools.proxies.MaterialPackageProxy(
            'experimental.tools.scoremanagertools.materialpackages.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.list_directory() == [
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
            'experimental.tools.scoremanagertools.materialpackages.testnotes')


def test_MaterialPackageWrangler_make_handmade_material_package_02():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert wrangler.configuration.packagesystem_path_exists(
        'experimental.tools.scoremanagertools.materialpackages.red_notes')
    assert py.test.raises(Exception, 'wrangler.make_handmade_material_package'
        "('experimental.tools.scoremanagertools.materialpackages.red_notes')")


def test_MaterialPackageWrangler_make_handmade_material_package_03():
    r'''Interactively.
    '''

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists(
        'experimental.tools.scoremanagertools.materialpackages.testnotes')


    try:
        wrangler.interactively_make_handmade_material_package(pending_user_input='testnotes q')
        assert wrangler.configuration.packagesystem_path_exists(
            'experimental.tools.scoremanagertools.materialpackages.testnotes')
        mpp = scoremanagertools.proxies.MaterialPackageProxy(
            'experimental.tools.scoremanagertools.materialpackages.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists(
            'experimental.tools.scoremanagertools.materialpackages.testnotes')


def test_MaterialPackageWrangler_make_handmade_material_package_04():
    r'''With custom tags.
    '''

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists(
        'experimental.tools.scoremanagertools.materialpackages.testnotes')


    try:
        tags = {'color': 'red', 'is_colored': True}
        wrangler.make_handmade_material_package(
            'experimental.tools.scoremanagertools.materialpackages.testnotes', tags=tags)
        assert wrangler.configuration.packagesystem_path_exists(
            'experimental.tools.scoremanagertools.materialpackages.testnotes')
        mpp = scoremanagertools.proxies.MaterialPackageProxy(
            'experimental.tools.scoremanagertools.materialpackages.testnotes')
        assert mpp.get_tag('color') == 'red'
        assert mpp.get_tag('is_colored')
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists(
            'experimental.tools.scoremanagertools.materialpackages.testnotes')
