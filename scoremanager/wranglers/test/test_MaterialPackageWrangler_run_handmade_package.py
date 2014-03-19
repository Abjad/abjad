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
boilerplate_definition_module_path = os.path.join(
    configuration.boilerplate_directory_path,
    'boilerplate_testnotes_definition.py',
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
    r'''Makes handmade package. Corrupts initializer. Restores initializer.
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
    r'''Makes handmade package. Copies canned material definition. 
    Makes output module. Removes output material. Removes package.
    '''

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
        assert os.path.exists(definition_module_path)
        assert os.path.exists(output_module_path)
        input_ = 'lmm testnotes omrm remove q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(definition_module_path)
        assert not os.path.exists(output_module_path)
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(package_path)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_run_handmade_package_08():
    r'''Makes handmade package. Corrupts definition module. Makes sure
    score manager starts when definition module is corrupt. Removes package.
    '''

    assert not os.path.exists(package_path)
    try:
        input_ = 'lmm nmh testnotes q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        assert os.path.exists(definition_module_path)
        shutil.copyfile(exception_file_path, definition_module_path)
        assert filecmp.cmp(definition_module_path, exception_file_path)
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(package_path)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_run_handmade_package_09():
    r'''Makes handmade package. Copies canned material definition module. 
    Makes output module. Corrupts output module. Makes sure score manager 
    starts when output module is corrupt. Removes package.
    '''

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
        assert filecmp.cmp(
            definition_module_path,
            boilerplate_definition_module_path,
            )
        input_ = 'lmm testnotes omw default q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(output_module_path)
        assert not filecmp.cmp(output_module_path, exception_file_path)
        shutil.copyfile(exception_file_path, output_module_path)
        assert filecmp.cmp(output_module_path, exception_file_path)
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(package_path)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_run_handmade_package_10():
    r'''Makes handmade package. Copies canned material definition module.
    Makes output data. Makes PDF. Removes package.
    '''
    pytest.skip('make PDF generation work again.')

    assert not os.path.exists(package_path)
    try:
        input_ = 'lmm nmh testnotes q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        assert os.path.exists(definition_module_path)
        shutil.copyfile(
            boilerplate_definition_module_path,
            definition_module_path,
            )
        input_ = 'lmm testnotes omw q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(output_module_path)
        input_ = 'lmm testnotes pdfm default q'
        pdf_file_path = os.path.join(package_path, 'illustration.pdf')
        ly_file_path = os.path.join(package_path, 'illustration.ly')
        assert os.path.exists(pdf_file_path)
        assert os.path.exists(ly_file_path)
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(package_path)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)