# -*- encoding: utf-8 -*-
import os
import pytest
import shutil
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_MaterialPackageWrangler_make_handmade_material_package_01():
    r'''Package is created and directory contents are correct.
    '''

    session = scoremanager.core.Session()
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'material_definition.py', 
        ]
    input_ = 'testnotes q'

    assert not os.path.exists(path)
    try:
        wrangler.make_handmade_material_package(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_MaterialPackageWrangler_make_handmade_material_package_02():
    r'''Empty material definition module is correct.
    '''

    score_manager = scoremanager.core.ScoreManager()
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    material_definition_module_path = os.path.join(
        path,
        'material_definition.py',
        )
    input_ = 'lmm nmh testnotes q'

    lines = []
    lines.append('# -*- encoding: utf-8 -*-')
    lines.append('from abjad import *')
    lines.append('_output_material_module_import_statements = []')
    lines.append('')
    lines.append('')
    lines.append('testnotes = None')
    contents = '\n'.join(lines)

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_, is_test=True)
        assert os.path.exists(path)
        file_pointer = file(material_definition_module_path, 'r')
        file_lines = file_pointer.readlines()
        file_pointer.close()
        file_contents = ''.join(file_lines)
        assert file_contents == contents
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)
