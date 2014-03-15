# -*- encoding: utf-8 -*-
import os
import pytest
import shutil
from abjad import *
import scoremanager


def test_MaterialPackageWrangler__make_data_package_01():

    session = scoremanager.core.Session()
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)
    path = os.path.join(
        wrangler._configuration.user_library_material_packages_directory_path,
        'testnumbers',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'material_definition.py', 
        ]

    assert not os.path.exists(path)
    try:
        wrangler._make_data_package(path)
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        assert manager._interpret_definition_module() is None
        output_material = manager._execute_output_material_module()
        assert output_material is None
        manager._remove()
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_MaterialPackageWrangler__make_data_package_02():
    r'''With custom metadata.
    '''

    session = scoremanager.core.Session()
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)
    path = os.path.join(
        wrangler._configuration.user_library_material_packages_directory_path,
        'testnumbers',
        )

    assert not os.path.exists(path)
    try:
        metadata = {'color': 'red', 'is_colored': True}
        wrangler._make_data_package(path, metadata=metadata)
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=path, session=session)
        assert manager._get_metadatum('color') == 'red'
        assert manager._get_metadatum('is_colored')
        manager._remove()
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)
