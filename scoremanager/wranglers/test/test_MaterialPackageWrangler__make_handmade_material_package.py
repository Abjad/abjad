# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler__make_handmade_material_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    path = os.path.join(
        wrangler._configuration.abjad_material_packages_directory_path,
        'testnotes',
        )
    assert not os.path.exists(path)
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'material_definition.py', 
        ]

    try:
        wrangler._make_handmade_material_package(path)
        assert os.path.exists(path)
        manager = scoremanager.managers.MaterialManager(path)
        assert manager._list() == directory_entries
        assert manager._interpret_material_definition_module() is None
        output_material = manager._execute_output_material_module()
        assert output_material is None
    finally:
        manager._remove()
        assert not os.path.exists(path)


def test_MaterialPackageWrangler__make_handmade_material_package_03():
    r'''With custom metadata.
    '''

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    path = os.path.join(
        wrangler._configuration.abjad_material_packages_directory_path,
        'testnotes',
        )
    assert not os.path.exists(path)

    try:
        metadata = {'color': 'red', 'is_colored': True}
        wrangler._make_handmade_material_package(
            path, 
            metadata=metadata,
            )
        assert os.path.exists(path)
        manager = scoremanager.managers.MaterialManager(path)
        assert manager._get_metadatum('color') == 'red'
        assert manager._get_metadatum('is_colored')
    finally:
        manager._remove()
        assert not os.path.exists(path)
