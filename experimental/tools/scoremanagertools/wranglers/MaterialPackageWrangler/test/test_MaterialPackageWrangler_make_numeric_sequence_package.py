# -*- encoding: utf-8 -*-
from experimental import *


def test_MaterialPackageWrangler_make_numeric_sequence_package_01():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testsequence')

    try:
        wrangler.make_numeric_sequence_package('experimental.tools.scoremanagertools.materialpackages.testsequence')
        assert wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testsequence')
        mpp = scoremanagertools.proxies.MaterialPackageProxy('experimental.tools.scoremanagertools.materialpackages.testsequence')
        assert mpp.is_data_only
        assert mpp.list_directory() == ['__init__.py', 'material_definition.py', 'tags.py']
        assert mpp.get_tag('is_numeric_sequence')
        assert mpp.get_tag('is_material_package')
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testsequence')


def test_MaterialPackageWrangler_make_numeric_sequence_package_02():
    r'''Interactively.
    '''

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testsequence')

    try:
        wrangler.interactively_make_numeric_sequence_package(pending_user_input='testsequence')
        assert wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testsequence')
        mpp = scoremanagertools.proxies.MaterialPackageProxy('experimental.tools.scoremanagertools.materialpackages.testsequence')
        assert mpp.is_data_only
        assert mpp.list_directory() == ['__init__.py', 'material_definition.py', 'tags.py']
        assert mpp.get_tag('is_numeric_sequence')
        assert mpp.get_tag('is_material_package')
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testsequence')
