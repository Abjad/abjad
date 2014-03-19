# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)
configuration = scoremanager.core.ScoreManagerConfiguration()
package_path = os.path.join(
    configuration.user_library_material_packages_directory_path,
    'testsargasso',
    )
initializer_file_path = os.path.join(package_path, '__init__.py')

exception_file_path = os.path.join(
    configuration.boilerplate_directory_path,
    'boilerplate_exception.py',
    )
empty_unicode_file_path = os.path.join(
    configuration.boilerplate_directory_path,
    'empty_unicode_file.py',
    )


def test_MaterialPackageWrangler_run_managermade_package_01():
    r'''Makes managermade package. Removes package.
    '''

    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'user_input.py',
        ]

    assert not os.path.exists(package_path)
    try:
        input_ = 'lmm nmm sargasso testsargasso default q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.SargassoMeasureMaterialManager
        manager = manager(path=package_path, session=session)
        assert manager._list() == directory_entries
        input_ = 'lmm testsargasso rm remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(package_path)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_run_managermade_package_02():
    r'''Makes managermade package. Corrupts initializer. Removes package.
    '''

    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'user_input.py',
        ]

    assert not os.path.exists(package_path)
    try:
        input_ = 'lmm nmm sargasso testsargasso q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        assert os.path.exists(initializer_file_path)
        assert filecmp.cmp(initializer_file_path, empty_unicode_file_path)
        shutil.copyfile(exception_file_path, initializer_file_path)
        assert filecmp.cmp(initializer_file_path, exception_file_path)
        input_ = 'lmm testsargasso rm remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(package_path)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_run_managermade_package_03():
    r'''Makes managermade package. Corrupts initializer. Restores initializer.
    Removes package.
    '''

    assert not os.path.exists(package_path)
    try:
        input_ = 'lmm nmm sargasso testsargasso q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        assert os.path.exists(initializer_file_path)
        assert filecmp.cmp(initializer_file_path, empty_unicode_file_path)
        shutil.copyfile(exception_file_path, initializer_file_path)
        assert filecmp.cmp(initializer_file_path, exception_file_path)
        input_ = 'lmm testsargasso ins default q'
        score_manager._run(pending_user_input=input_)
        assert filecmp.cmp(initializer_file_path, empty_unicode_file_path)
        input_ = 'lmm testsargasso rm remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(package_path)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)


def test_MaterialPackageWrangler_run_managermade_package_04():
    r'''Makes score-resident managermade package. Makes sure initializer,
    metadata module and user input module are created. Removes package.
    '''

    package_path = os.path.join(
        configuration.abjad_score_packages_directory_path,
        'red_example_score',
        'materials',
        'testsargasso',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'user_input.py',
        ]

    assert not os.path.exists(package_path)
    try:
        input_ = 'red~example~score m nmm sargasso testsargasso default q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(package_path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.SargassoMeasureMaterialManager
        manager = manager(path=package_path, session=session)
        assert manager._list() == directory_entries
        input_ = 'red~example~score m testsargasso rm remove q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(package_path)
    finally:
        if os.path.exists(package_path):
            shutil.rmtree(package_path)
    assert not os.path.exists(package_path)