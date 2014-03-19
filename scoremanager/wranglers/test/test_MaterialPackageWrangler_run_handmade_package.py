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
    'boilerplate_exception.py',
    )
empty_unicode_file_path = os.path.join(
    configuration.boilerplate_directory_path,
    'empty_unicode_file.py',
    )


def test_MaterialPackageWrangler_run_handmade_package_01():
    r'''Makes handmade package. Makes sure initializer, metadata module and
    definition module are created. Removes package.
    '''

    assert not os.path.exists(package_path)
    try:
        input_ = 'lmm nmh testnotes q'
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


def test_MaterialPackageWrangler_run_handmade_package_02():
    r'''Makes handmade package. Corrupts initializer. Makes sure score manager
    starts and package is removable when initializer is corrupt.
    Removes package.
    '''

    assert not os.path.exists(package_path)
    try:
        input_ = 'lmm nmh testnotes q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        assert os.path.exists(initializer_file_path)
        assert filecmp.cmp(initializer_file_path, empty_unicode_file_path)
        shutil.copyfile(exception_file_path, initializer_file_path)
        assert filecmp.cmp(initializer_file_path, exception_file_path)
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(package_path)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_run_handmade_package_03():
    r'''Makes handmade package. Corrupts initializer. Makes sure score
    manager starts and initializer is restorable when initializer is corrupt.
    Restores initializer.
    '''

    assert not os.path.exists(package_path)
    try:
        input_ = 'lmm nmh testnotes q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        assert os.path.exists(initializer_file_path)
        assert filecmp.cmp(initializer_file_path, empty_unicode_file_path)
        shutil.copyfile(exception_file_path, initializer_file_path)
        assert filecmp.cmp(initializer_file_path, exception_file_path)
        input_ = 'lmm testnotes ins default q'
        score_manager._run(pending_user_input=input_)
        assert filecmp.cmp(initializer_file_path, empty_unicode_file_path)
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(package_path)
        assert not os.path.exists(initializer_file_path)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_run_handmade_package_04():
    r'''Makes handmade package. Copies boilerplate definition module.
    Creates output material. Removes package.
    '''

    boilerplate_definition_module_path = os.path.join(
        configuration.boilerplate_directory_path,
        'boilerplate_testnotes_definition.py',
        )

    assert not os.path.exists(package_path)
    try:
        input_ = 'lmm nmh testnotes q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        assert os.path.exists(definition_module_path)
        assert not os.path.exists(output_module_path)
        shutil.copyfile(
            boilerplate_definition_module_path,
            definition_module_path,
            )
        input_ = 'lmm testnotes omw default q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(output_module_path)
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(package_path)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_run_handmade_package_05():
    r'''Makes handmade package. Removes definition module. Removes package.
    '''

    assert not os.path.exists(package_path)
    try:
        input_ = 'lmm nmh testnotes q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        assert os.path.exists(definition_module_path)
        input_ = 'lmm testnotes dmrm remove q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        assert not os.path.exists(definition_module_path)
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(package_path)
        assert not os.path.exists(definition_module_path)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_run_handmade_package_06():
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
        input_ = 'lmm nmh testnotes default testnotes dms default q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=package_path, session=session)
        assert manager._list() == directory_entries
        assert manager._interpret_definition_module() is None
        assert manager._execute_output_module() is None
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_run_handmade_package_07():
    r'''Make handmade package. Copy canned material definition. 
    Make output material. Remove output material. Remove package.
    '''

    package_path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'definition.py', 
        ]

    assert not os.path.exists(package_path)
    try:
        input_ = 'lmm nmh testnotes'
        input_ += ' testnotes dmbp boilerplate_testnotes_definition.py'
        input_ += ' default omw default omrm remove q' 
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=package_path, session=session)
        assert manager._list() == directory_entries
        material_definition = manager._interpret_definition_module()
        assert material_definition
        assert all(isinstance(x, Note) for x in material_definition)
        output_material = manager._execute_output_module()
        assert output_material is None
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_run_handmade_package_08():
    r'''Make handmade package. Copy canned material definition with exception.
    Examine package state. Remove package.
    '''

    package_path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'definition.py', 
        ]

    assert not os.path.exists(package_path)
    try:
        input_ = 'lmm nmh testnotes default default'
        input_ += ' testnotes dmbp boilerplate_exception.py default q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=package_path, session=session)
        assert manager._list() == directory_entries
        assert manager._interpret_definition_module() is None
        assert manager._execute_output_module() is None
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_run_handmade_package_09():
    r'''Make handmade package. Copy canned material definition module. 
    Make output data. Corrupt output data. Verify invalid output material 
    module. Remove package.
    '''

    package_path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py', 
        'output.py', 
        ]

    assert not os.path.exists(package_path)
    try:
        input_ = 'lmm nmh testnotes default default testnotes dmbp'
        input_ += ' boilerplate_testnotes_definition.py default '
        input_ += 'omw default ombp boilerplate_exception.py default q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=package_path, session=session)
        assert manager._list() == directory_entries
        material_definition = manager._interpret_definition_module()
        assert material_definition
        assert all(isinstance(x, Note) for x in material_definition)
        output_material = manager._execute_output_module()
        assert output_material is None
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_run_handmade_package_10():
    r'''Make handmade package. Copy canned material definition module.
    Make output data. Make PDF. Remove package.
    '''
    pytest.skip('make PDF generation work again.')

    package_path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'illustration.ly', 
        'illustration.pdf',
        ]

    assert not os.path.exists(package_path)
    try:
        input_ = 'lmm nmh testnotes testnotes dmbp'
        input_ += ' boilerplate_testnotes_definition.py default'
        input_ += ' omw default pdfm default q' 
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=package_path, session=session)
        assert manager._list() == directory_entries
        material_definition = manager._interpret_definition_module()
        assert material_definition
        assert all(isinstance(x, Note) for x in material_definition)
        output_material = manager._execute_output_module()
        assert output_material
        assert all(isinstance(x, Note) for x in output_material)
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)
