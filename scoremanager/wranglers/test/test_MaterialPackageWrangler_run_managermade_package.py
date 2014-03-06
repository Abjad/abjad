# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_run_managermade_package_01():
    r'''Make managermade package. Delete package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    path = os.path.join(
        score_manager._configuration.abjad_material_packages_directory_path,
        'testsargasso',
        )
    assert not os.path.exists(path)
    input_ = 'lmm nmm sargasso testsargasso default q'
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'user_input.py',
        ]

    try:
        score_manager._run(pending_user_input=input_, is_test=True)
        assert os.path.exists(path)
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            path=path)
        assert manager._list() == directory_entries
    finally:
        input_ = 'lmm testsargasso rm remove q'
        score_manager._run(pending_user_input=input_, is_test=True)
        assert not os.path.exists(path)


def test_MaterialPackageWrangler_run_managermade_package_02():
    r'''Make score-resident managermade package. Delete package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    path = os.path.join(
        score_manager._configuration.abjad_score_packages_directory_path,
        'red_example_score',
        'materials',
        'testsargasso',
        )
    assert not os.path.exists(path)
    input_ = 'red~example~score m nmm sargasso testsargasso default q'
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'user_input.py',
        ]

    try:
        score_manager._run(pending_user_input=input_, is_test=True)
        assert os.path.exists(path)
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            path=path)
        assert manager._list() == directory_entries
    finally:
        input_ = 'red~example~score m testsargasso rm remove q'
        score_manager._run(pending_user_input=input_, is_test=True)
        assert not os.path.exists(path)


def test_MaterialPackageWrangler_run_managermade_package_03():
    r'''Make managermade package. Corrupt initializer.
    Verify invalid initializer. Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    path = os.path.join(
        score_manager._configuration.abjad_material_packages_directory_path,
        'testsargassomeasures',
        )
    assert not os.path.exists(path)
    input_ = 'lmm nmm sargasso testsargassomeasures'
    input_ += ' testsargassomeasures inbp boilerplate_exception.py default q'
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'user_input.py',
        ]

    try:
        score_manager._run(pending_user_input=input_, is_test=True)
        assert os.path.exists(path)
        manager = scoremanager.managers.SargassoMeasureMaterialManager(path)
        assert manager._list() == directory_entries
        assert manager._interpret_material_definition_module() is None
        assert manager._execute_output_material_module() is None
    finally:
        input_ = 'lmm testsargassomeasures rm remove q'
        score_manager._run(pending_user_input=input_, is_test=True)
        assert not os.path.exists(path)


def test_MaterialPackageWrangler_run_managermade_package_04():
    r'''Make managermade package. Corrupt initializer. Restore initializer.
    Verify initializer. Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    path = os.path.join(
        score_manager._configuration.abjad_material_packages_directory_path,
        'testsargassomeasures',
        )
    assert not os.path.exists(path)
    input_ = 'lmm nmm sargasso testsargassomeasures'
    input_ += ' omi inbp boilerplate_exception.py default'
    input_ += ' ins default q'
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'user_input.py',
        ]

    try:
        score_manager._run(pending_user_input=input_, is_test=True)
        assert os.path.exists(path)
        manager = scoremanager.managers.SargassoMeasureMaterialManager(path)
        assert manager._list() == directory_entries
        assert manager._interpret_material_definition_module() is None
        assert manager._execute_output_material_module() is None
    finally:
        input_ = 'lmm testsargassomeasures rm remove q'
        score_manager._run(pending_user_input=input_, is_test=True)
        assert not os.path.exists(path)
