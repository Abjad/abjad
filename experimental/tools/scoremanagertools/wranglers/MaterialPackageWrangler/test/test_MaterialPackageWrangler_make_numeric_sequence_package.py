from experimental import *


def test_MaterialPackageWrangler_make_numeric_sequence_package_01():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testsequence')

    try:
        wrangler.make_numeric_sequence_package('experimental.tools.scoremanagertools.built_in_materials.testsequence')
        assert wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testsequence')
        mpp = scoremanagertools.proxies.MaterialPackageProxy('experimental.tools.scoremanagertools.built_in_materials.testsequence')
        assert mpp.is_data_only
        assert mpp.list_directory() == ['__init__.py', 'material_definition.py', 'tags.py']
        assert mpp.get_tag('is_numeric_sequence')
        assert mpp.get_tag('is_material_package')
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testsequence')


def test_MaterialPackageWrangler_make_numeric_sequence_package_02():
    '''Interactively.
    '''

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testsequence')

    try:
        wrangler.make_numeric_sequence_package_interactively(user_input='testsequence')
        assert wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testsequence')
        mpp = scoremanagertools.proxies.MaterialPackageProxy('experimental.tools.scoremanagertools.built_in_materials.testsequence')
        assert mpp.is_data_only
        assert mpp.list_directory() == ['__init__.py', 'material_definition.py', 'tags.py']
        assert mpp.get_tag('is_numeric_sequence')
        assert mpp.get_tag('is_material_package')
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testsequence')
