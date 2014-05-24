# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_MaterialPackageWrangler__make_material_package_01():

    session = scoremanager.core.Session(is_test=True)
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)
    path = os.path.join(
        wrangler._configuration.user_library_material_packages_directory,
        'testnumbers',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        ]

    with systemtools.FilesystemState(remove=[path]):
        wrangler._make_package(path)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        assert manager._interpret_definition_py() is None
        output_material = manager._execute_output_py()
        assert output_material is None
        manager._session._confirm = False
        manager._remove()


def test_MaterialPackageWrangler__make_material_package_02():

    session = scoremanager.core.Session(is_test=True)
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)
    path = os.path.join(
        wrangler._configuration.user_library_material_packages_directory,
        'testnotes',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        ]

    with systemtools.FilesystemState(remove=[path]):
        wrangler._make_package(path)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        assert manager._interpret_definition_py() is None
        output_material = manager._execute_output_py()
        assert output_material is None
        manager._session._confirm = False
        manager._remove()