import py
from experimental import *


def test_MaterialPackageWrangler_make_handmade_material_package_01():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testnotes')


    try:
        wrangler.make_handmade_material_package('experimental.tools.scoremanagertools.built_in_materials.testnotes')
        assert wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testnotes')
        mpp = scoremanagertools.proxies.MaterialPackageProxy('experimental.tools.scoremanagertools.built_in_materials.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.list_directory() == ['__init__.py', 'material_definition.py', 'tags.py']
        assert mpp.has_readable_initializer
        assert mpp.has_readable_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        #assert not mpp.initializer_has_output_material_safe_import_statement
        #assert not mpp.parent_initializer_has_output_material_safe_import_statement
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testnotes')


def test_MaterialPackageWrangler_make_handmade_material_package_02():

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.red_notes')
    assert py.test.raises(Exception, "wrangler.make_handmade_material_package('experimental.tools.scoremanagertools.built_in_materials.red_notes')")


def test_MaterialPackageWrangler_make_handmade_material_package_03():
    '''Interactively.
    '''

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testnotes')


    try:
        wrangler.make_handmade_material_package_interactively(user_input='testnotes q')
        assert wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testnotes')
        mpp = scoremanagertools.proxies.MaterialPackageProxy('experimental.tools.scoremanagertools.built_in_materials.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.list_directory() == ['__init__.py', 'material_definition.py', 'tags.py']
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testnotes')


def test_MaterialPackageWrangler_make_handmade_material_package_04():
    '''With custom tags.
    '''

    wrangler = scoremanagertools.wranglers.MaterialPackageWrangler()
    assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testnotes')


    try:
        tags = {'color': 'red', 'is_colored': True}
        wrangler.make_handmade_material_package('experimental.tools.scoremanagertools.built_in_materials.testnotes', tags=tags)
        assert wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testnotes')
        mpp = scoremanagertools.proxies.MaterialPackageProxy('experimental.tools.scoremanagertools.built_in_materials.testnotes')
        assert mpp.get_tag('color') == 'red'
        assert mpp.get_tag('is_colored')
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.built_in_materials.testnotes')
