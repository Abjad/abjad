# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager



def test_MaterialPackageWrangler__make_managermade_material_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    path = os.path.join(
        wrangler._configuration.abjad_material_packages_directory_path,
        'testsargasso',
        )
    assert not os.path.exists(path)
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'user_input.py',
        ]

    try:
        wrangler._make_managermade_material_package(
            path, 
            'SargassoMeasureMaterialManager',
            )
        assert os.path.exists(path)
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            path=path)
        assert manager._list() == directory_entries
    finally:
        manager._remove()
        assert not os.path.exists(path)


def test_MaterialPackageWrangler__make_managermade_material_package_03():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    path = os.path.join(
        wrangler._configuration.abjad_material_packages_directory_path,
        'testsargasso',
        )
    assert not os.path.exists(path)
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'user_input.py',
        ]

    try:
        metadata = {'color': 'red', 'is_colored': True}
        wrangler._make_managermade_material_package(
            path, 
            'SargassoMeasureMaterialManager', 
            metadata=metadata,
            )
        assert os.path.exists(path)
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            path=path)
        assert manager._list() == directory_entries
        assert manager._get_metadatum('color') == 'red'
        assert manager._get_metadatum('is_colored')
    finally:
        manager._remove()
        assert not os.path.exists(path)
