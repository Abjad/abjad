import py
from experimental import *


def test_MaterialPackageWrangler_make_data_package_01():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testnumbers')

    try:
        wrangler.make_data_package('experimental.tools.scoremanagertools.built_in_materials.testnumbers')
        assert wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testnumbers')
        mpp = scoremanagertools.proxies.MaterialPackageProxy('experimental.tools.scoremanagertools.built_in_materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.list_directory() == ['__init__.py', 'material_definition.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert mpp.has_readable_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.initializer_has_output_material_safe_import_statement
        assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testnumbers')


def test_MaterialPackageWrangler_make_data_package_02():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.red_numbers')
    assert py.test.raises(Exception, "wrangler.make_data_package('experimental.tools.scoremanagertools.built_in_materials.red_numbers')")


def test_MaterialPackageWrangler_make_data_package_03():
    '''Interactively.
    '''

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testnumbers')

    try:
        wrangler.make_data_package_interactively(user_input='testnumbers q')
        assert wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testnumbers')
        mpp = scoremanagertools.proxies.MaterialPackageProxy('experimental.tools.scoremanagertools.built_in_materials.testnumbers')
        assert mpp.is_data_only
        assert mpp.list_directory() == ['__init__.py', 'material_definition.py', 'tags.py']
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testnumbers')


def test_MaterialPackageWrangler_make_data_package_04():
    '''With custom tags.
    '''

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testnumbers')

    try:
        tags = {'color': 'red', 'is_colored': True}
        wrangler.make_data_package('experimental.tools.scoremanagertools.built_in_materials.testnumbers', tags=tags)
        assert wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testnumbers')
        mpp = scoremanagertools.proxies.MaterialPackageProxy('experimental.tools.scoremanagertools.built_in_materials.testnumbers')
        assert mpp.get_tag('color') == 'red'
        assert mpp.get_tag('is_colored')
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testnumbers')
