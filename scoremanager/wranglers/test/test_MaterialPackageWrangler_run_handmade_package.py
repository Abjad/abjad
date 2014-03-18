# -*- encoding: utf-8 -*-
import os
import pytest
import shutil
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_MaterialPackageWrangler_run_handmade_package_01():
    r'''Make handmade package. Delete package.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'material_definition.py', 
        ]

    assert not os.path.exists(path)
    try:
        input_ = 'lmm nmh testnotes default default q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        assert manager._interpret_definition_module() is None
        assert manager._execute_output_module() is None
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_MaterialPackageWrangler_run_handmade_package_02():
    r'''Make handmade package. Corrupt initializer.
    Verify invalid initializer. Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'material_definition.py', 
        ]
    input_ = 'lmm nmh testnotes'
    input_ += ' testnotes inbp boilerplate_exception.py default q'

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._interpret_definition_module()
        assert output_material is None
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_MaterialPackageWrangler_run_handmade_package_03():
    r'''Make handmade package. Corrupt initializer. Restore initializer.
    Verify initializer. Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'material_definition.py', 
        ]
    input_ = 'lmm nmh testnotes'
    input_ += ' testnotes inbp boilerplate_exception.py default'
    input_ += ' inr yes yes default q'

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        assert manager._interpret_definition_module() is None
        assert manager._execute_output_module() is None
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_MaterialPackageWrangler_run_handmade_package_04():
    r'''Make handmade package. Create output material.
    Delete package."
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'material_definition.py', 
        'output_material.py', 
        ]
    input_ = 'lmm nmh testnotes default default testnotes dmbp'
    input_ += ' boilerplate_testnotes_material_definition.py default'
    input_ += ' omw default q'

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=path, session=session)
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
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_MaterialPackageWrangler_run_handmade_package_05():
    r'''Make handmade package. Delete material definition module.
    Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        ]
    input_ = 'lmm nmh testnotes testnotes dmrm remove q'

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_MaterialPackageWrangler_run_handmade_package_06():
    r'''Make handmade package. Overwrite material definition module with stub.
    Delete package.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'material_definition.py', 
        ]
    input_ = 'lmm nmh testnotes default testnotes dms default q'

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        assert manager._interpret_definition_module() is None
        assert manager._execute_output_module() is None
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_MaterialPackageWrangler_run_handmade_package_07():
    r'''Make handmade package. Copy canned material definition. 
    Make output material. Remove output material. Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'material_definition.py', 
        ]
    input_ = 'lmm nmh testnotes'
    input_ += ' testnotes dmbp boilerplate_testnotes_material_definition.py'
    input_ += ' default omw default omrm remove q' 

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        material_definition = manager._interpret_definition_module()
        assert material_definition
        assert all(isinstance(x, Note) for x in material_definition)
        output_material = manager._execute_output_module()
        assert output_material is None
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_MaterialPackageWrangler_run_handmade_package_08():
    r'''Make handmade package. Copy canned material definition with exception.
    Examine package state. Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'material_definition.py', 
        ]
    input_ = 'lmm nmh testnotes default default'
    input_ += ' testnotes dmbp boilerplate_exception.py default q'

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        assert manager._interpret_definition_module() is None
        assert manager._execute_output_module() is None
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_MaterialPackageWrangler_run_handmade_package_09():
    r'''Make handmade package. Copy canned material definition module. 
    Make output data. Corrupt output data. Verify invalid output material 
    module. Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'material_definition.py', 
        'output_material.py', 
        ]
    input_ = 'lmm nmh testnotes default default testnotes dmbp'
    input_ += ' boilerplate_testnotes_material_definition.py default '
    input_ += 'omw default ombp boilerplate_exception.py default q'

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        material_definition = manager._interpret_definition_module()
        assert material_definition
        assert all(isinstance(x, Note) for x in material_definition)
        output_material = manager._execute_output_module()
        assert output_material is None
        input_ = 'lmm testnotes rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)


def test_MaterialPackageWrangler_run_handmade_package_10():
    r'''Make handmade package. Copy canned material definition module.
    Make output data. Make PDF. Remove package.
    '''
    pytest.skip('make PDF generation work again.')

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testnotes',
        )
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'illustration.ly', 
        'illustration.pdf',
        ]
    input_ = 'lmm nmh testnotes testnotes dmbp'
    input_ += ' boilerplate_testnotes_material_definition.py default'
    input_ += ' omw default pdfm default q' 

    assert not os.path.exists(path)
    try:
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session()
        manager = scoremanager.managers.MaterialManager
        manager = manager(path=path, session=session)
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
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)
