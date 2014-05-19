# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)

package_path = os.path.join(
    score_manager._configuration.user_library_material_packages_directory_path,
    'testnotes',
    )
initializer_file_path = os.path.join(package_path, '__init__.py')
metadata_py_path = os.path.join(package_path, '__metadata__.py')
definition_py_path = os.path.join(package_path, 'definition.py')
output_py_path = os.path.join(package_path, 'output.py')

exception_file_path = os.path.join(
    score_manager._configuration.boilerplate_directory_path,
    'exception.py',
    )
empty_unicode_file_path = os.path.join(
    score_manager._configuration.boilerplate_directory_path,
    'empty_unicode.py',
    )
boilerplate_definition_py_path = os.path.join(
    score_manager._configuration.boilerplate_directory_path,
    'notes_definition.py',
    )


def test_MaterialPackageWrangler_make_package_01():
    r'''Back works in path getter.
    '''

    input_ = 'm new b q'
    score_manager._run(pending_input=input_)
    first_lines = [
        'Score manager - scores',
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
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        ]

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'testnotes q'
        wrangler._session._pending_input = input_
        wrangler.make_package()
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries


def test_MaterialPackageWrangler_make_package_03():
    r'''Creates empty material definition py.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    definition_py_path = os.path.join(
        path,
        'definition.py',
        )

    lines = []
    lines.append('# -*- encoding: utf-8 -*-')
    lines.append('from abjad import *')
    lines.append('output_py_import_statements = []')
    lines.append('')
    lines.append('')
    lines.append('testnotes = None')
    contents = '\n'.join(lines)

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'm new testnotes q'
        score_manager._run(pending_input=input_)
        assert os.path.exists(path)
        with file(definition_py_path, 'r') as file_pointer:
            file_lines = file_pointer.readlines()
        file_contents = ''.join(file_lines)
        assert file_contents == contents


def test_MaterialPackageWrangler_make_package_04():
    r'''Makes handmade package. Makes sure __init__.py, __metadata__.py and
    definition.py are created. Removes package.
    '''

    with systemtools.FilesystemState(remove=[package_path]):
        input_ = 'm new testnotes q'
        score_manager._run(pending_input=input_)
        assert os.path.exists(package_path)
        assert os.path.exists(initializer_file_path)
        assert os.path.exists(metadata_py_path)
        assert os.path.exists(definition_py_path)


def test_MaterialPackageWrangler_make_package_05():
    r'''Makes handmade package. Corrupts __init__.py. Makes sure score manager
    starts and package is removable when __init__.py is corrupt.
    Removes package.
    '''

    with systemtools.FilesystemState(remove=[package_path]):
        input_ = 'm new testnotes q'
        score_manager._run(pending_input=input_)
        assert os.path.exists(package_path)
        assert os.path.exists(initializer_file_path)
        assert filecmp.cmp(initializer_file_path, empty_unicode_file_path)
        shutil.copyfile(exception_file_path, initializer_file_path)
        assert filecmp.cmp(initializer_file_path, exception_file_path)
        input_ = 'm rm testnotes remove q'
        score_manager._run(pending_input=input_)
        assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_make_package_06():
    r'''Makes handmade package. Copies boilerplate definition py.
    Creates output material. Removes package.
    '''

    with systemtools.FilesystemState(remove=[package_path]):
        input_ = 'm new testnotes q'
        score_manager._run(pending_input=input_)
        assert os.path.exists(package_path)
        assert os.path.exists(definition_py_path)
        assert not os.path.exists(output_py_path)
        shutil.copyfile(
            boilerplate_definition_py_path,
            definition_py_path,
            )
        input_ = 'm testnotes omw y q'
        score_manager._run(pending_input=input_)
        assert os.path.exists(output_py_path)
        input_ = 'm rm testnotes remove q'
        score_manager._run(pending_input=input_)
        assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_make_package_07():
    r'''Makes handmade package. Overwrite material definition py with stub.
    Removes package.
    '''

    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        ]

    with systemtools.FilesystemState(remove=[package_path]):
        input_ = 'm new testnotes default testnotes dms default q'
        score_manager._run(pending_input=input_)
        assert os.path.exists(package_path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialPackageManager
        manager = manager(path=package_path, session=session)
        assert manager._list() == directory_entries
        assert manager._interpret_definition_py() is None
        assert manager._execute_output_py() is None
        input_ = 'm rm testnotes remove q'
        score_manager._run(pending_input=input_)


def test_MaterialPackageWrangler_make_package_08():
    r'''Makes handmade package. Corrupts definition py. Makes sure
    score manager starts when definition py is corrupt. Removes package.
    '''

    with systemtools.FilesystemState(remove=[package_path]):
        input_ = 'm new testnotes q'
        score_manager._run(pending_input=input_)
        assert os.path.exists(package_path)
        assert os.path.exists(definition_py_path)
        shutil.copyfile(exception_file_path, definition_py_path)
        assert filecmp.cmp(definition_py_path, exception_file_path)
        input_ = 'm rm testnotes remove q'
        score_manager._run(pending_input=input_)
        assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_make_package_09():
    r'''Makes handmade package. Copies canned material definition py.
    Makes output py. Corrupts output py. Makes sure score manager
    starts when output py is corrupt. Removes package.
    '''

    with systemtools.FilesystemState(remove=[package_path]):
        input_ = 'm new testnotes q'
        score_manager._run(pending_input=input_)
        assert os.path.exists(package_path)
        assert os.path.exists(definition_py_path)
        assert not os.path.exists(output_py_path)
        shutil.copyfile(
            boilerplate_definition_py_path,
            definition_py_path,
            )
        assert filecmp.cmp(
            definition_py_path,
            boilerplate_definition_py_path,
            )
        input_ = 'm testnotes omw y q'
        score_manager._run(pending_input=input_)
        assert os.path.exists(output_py_path)
        assert not filecmp.cmp(output_py_path, exception_file_path)
        shutil.copyfile(exception_file_path, output_py_path)
        assert filecmp.cmp(output_py_path, exception_file_path)
        input_ = 'm rm testnotes remove q'
        score_manager._run(pending_input=input_)
        assert not os.path.exists(package_path)