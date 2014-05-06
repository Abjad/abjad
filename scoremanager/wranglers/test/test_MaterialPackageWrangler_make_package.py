# -*- encoding: utf-8 -*-
import filecmp
import os
import pytest
import shutil
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()
score_manager = scoremanager.core.ScoreManager(is_test=True)

package_path = os.path.join(
    configuration.user_library_material_packages_directory_path,
    'testnotes',
    )
initializer_file_path = os.path.join(package_path, '__init__.py')
metadata_module_path = os.path.join(package_path, '__metadata__.py')
definition_module_path = os.path.join(package_path, 'definition.py')
output_module_path = os.path.join(package_path, 'output.py')

exception_file_path = os.path.join(
    configuration.boilerplate_directory_path,
    'exception.py',
    )
empty_unicode_file_path = os.path.join(
    configuration.boilerplate_directory_path,
    'empty_unicode.py',
    )
boilerplate_definition_module_path = os.path.join(
    configuration.boilerplate_directory_path,
    'notes_definition.py',
    )


def test_MaterialPackageWrangler_make_package_01():
    r'''Back works in path getter.
    '''

    input_ = 'm new b q'
    score_manager._run(pending_user_input=input_)
    first_lines = [
        'Score manager - example scores',
        '> m',
        'Score manager - materials',
        '> new',
        'Enter material package name> b',
        'Score manager - materials',
        '> q',
        ]
    
    assert score_manager._transcript.first_lines == first_lines


def test_MaterialPackageWrangler_make_package_02():
    r'''Creates package and populates package correctly.
    '''

    session = scoremanager.core.Session(is_test=True)
    wrangler = scoremanager.wranglers.MaterialPackageWrangler(session=session)
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        ]

    assert not os.path.exists(path)
    try:
        input_ = 'testnotes q'
        wrangler._session._pending_user_input = input_
        wrangler.make_package()
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_MaterialPackageWrangler_make_package_03():
    r'''Creates empty material definition module.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    definition_module_path = os.path.join(
        path,
        'definition.py',
        )

    lines = []
    lines.append('# -*- encoding: utf-8 -*-')
    lines.append('from abjad import *')
    lines.append('output_module_import_statements = []')
    lines.append('')
    lines.append('')
    lines.append('testnotes = None')
    contents = '\n'.join(lines)

    assert not os.path.exists(path)
    try:
        input_ = 'm new testnotes q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        with file(definition_module_path, 'r') as file_pointer:
            file_lines = file_pointer.readlines()
        file_contents = ''.join(file_lines)
        assert file_contents == contents
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_MaterialPackageWrangler_make_package_04():
    r'''Makes handmade package. Makes sure initializer, metadata module and
    definition module are created. Removes package.
    '''

    assert not os.path.exists(package_path)
    try:
        input_ = 'm new testnotes q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        assert os.path.exists(initializer_file_path)
        assert os.path.exists(metadata_module_path)
        assert os.path.exists(definition_module_path)
        shutil.rmtree(package_path)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_make_package_05():
    r'''Makes handmade package. Corrupts initializer. Makes sure score manager
    starts and package is removable when initializer is corrupt.
    Removes package.
    '''

    assert not os.path.exists(package_path)
    try:
        input_ = 'm new testnotes q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        assert os.path.exists(initializer_file_path)
        assert filecmp.cmp(initializer_file_path, empty_unicode_file_path)
        shutil.copyfile(exception_file_path, initializer_file_path)
        assert filecmp.cmp(initializer_file_path, exception_file_path)
        input_ = 'm rm testnotes remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(package_path)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_make_package_06():
    r'''Makes handmade package. Copies boilerplate definition module.
    Creates output material. Removes package.
    '''


    assert not os.path.exists(package_path)
    try:
        input_ = 'm new testnotes q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        assert os.path.exists(definition_module_path)
        assert not os.path.exists(output_module_path)
        shutil.copyfile(
            boilerplate_definition_module_path,
            definition_module_path,
            )
        input_ = 'm testnotes omw y q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(output_module_path)
        input_ = 'm rm testnotes remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(package_path)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_make_package_07():
    r'''Makes handmade package. Overwrite material definition module with stub.
    Removes package.
    '''

    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        ]

    assert not os.path.exists(package_path)
    try:
        input_ = 'm new testnotes default testnotes dms default q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialPackageManager
        manager = manager(path=package_path, session=session)
        assert manager._list() == directory_entries
        assert manager._interpret_definition_module() is None
        assert manager._execute_output_module() is None
        input_ = 'm rm testnotes remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_make_package_08():
    r'''Makes handmade package. Corrupts definition module. Makes sure
    score manager starts when definition module is corrupt. Removes package.
    '''

    assert not os.path.exists(package_path)
    try:
        input_ = 'm new testnotes q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        assert os.path.exists(definition_module_path)
        shutil.copyfile(exception_file_path, definition_module_path)
        assert filecmp.cmp(definition_module_path, exception_file_path)
        input_ = 'm rm testnotes remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(package_path)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_make_package_09():
    r'''Makes handmade package. Copies canned material definition module.
    Makes output module. Corrupts output module. Makes sure score manager
    starts when output module is corrupt. Removes package.
    '''

    assert not os.path.exists(package_path)
    try:
        input_ = 'm new testnotes q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        assert os.path.exists(definition_module_path)
        assert not os.path.exists(output_module_path)
        shutil.copyfile(
            boilerplate_definition_module_path,
            definition_module_path,
            )
        assert filecmp.cmp(
            definition_module_path,
            boilerplate_definition_module_path,
            )
        input_ = 'm testnotes omw y q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(output_module_path)
        assert not filecmp.cmp(output_module_path, exception_file_path)
        shutil.copyfile(exception_file_path, output_module_path)
        assert filecmp.cmp(output_module_path, exception_file_path)
        input_ = 'm rm testnotes remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(package_path)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)