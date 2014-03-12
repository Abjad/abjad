# -*- encoding: utf-8 -*-
import os
import pytest
import shutil
from abjad import *
import scoremanager



def test_MaterialPackageWrangler__make_managermade_material_package_01():

    session = scoremanager.core.Session()
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)
    path = os.path.join(
        wrangler._configuration.abjad_material_packages_directory_path,
        'testsargasso',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'user_input.py',
        ]

    assert not os.path.exists(path)
    try:
        wrangler._make_managermade_material_package(
            path, 
            'SargassoMeasureMaterialManager',
            )
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.SargassoMeasureMaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        manager._remove()
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_MaterialPackageWrangler__make_managermade_material_package_02():

    session = scoremanager.core.Session()
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)
    path = os.path.join(
        wrangler._configuration.abjad_material_packages_directory_path,
        'testsargasso',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'user_input.py',
        ]

    assert not os.path.exists(path)
    try:
        metadata = {'color': 'red', 'is_colored': True}
        wrangler._make_managermade_material_package(
            path, 
            'SargassoMeasureMaterialManager', 
            metadata=metadata,
            )
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.SargassoMeasureMaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        assert manager._get_metadatum('color') == 'red'
        assert manager._get_metadatum('is_colored')
        manager._remove()
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)
