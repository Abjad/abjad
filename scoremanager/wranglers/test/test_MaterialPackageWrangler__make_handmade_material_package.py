# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler__make_handmade_material_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.testnotes'
    assert not wrangler.configuration.package_exists(string)


    try:
        wrangler._make_handmade_material_package(string)
        assert wrangler.configuration.package_exists(string)
        manager = scoremanager.managers.MaterialPackageManager(string)
        assert manager._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not manager.has_output_material_module
        assert not manager.has_illustration_builder_module
        assert manager.material_definition is None
        assert manager.output_material is None
    finally:
        manager._remove()
        assert not wrangler.configuration.package_exists(string)


def test_MaterialPackageWrangler__make_handmade_material_package_02():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.red_notes'
    assert wrangler.configuration.package_exists(string)
    statement = 'wrangler._make_handmade_material_package'
    statement += "('scoremanager.materialpackages.red_notes')"
    assert pytest.raises(Exception, statement)


def test_MaterialPackageWrangler__make_handmade_material_package_03():
    r'''With custom metadata.
    '''

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.testnotes'
    assert not wrangler.configuration.package_exists(string)

    try:
        metadata = {'color': 'red', 'is_colored': True}
        wrangler._make_handmade_material_package(string, metadata=metadata)
        assert wrangler.configuration.package_exists(string)
        manager = scoremanager.managers.MaterialPackageManager(string)
        assert manager._get_metadatum('color') == 'red'
        assert manager._get_metadatum('is_colored')
    finally:
        manager._remove()
        assert not wrangler.configuration.package_exists(string)
