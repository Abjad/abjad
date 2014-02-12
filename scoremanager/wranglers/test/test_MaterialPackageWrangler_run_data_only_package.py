# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_run_data_only_package_01():
    r'''Make data package. Delete package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanager.materialpackages.testnumbers')

    try:
        score_manager._run(pending_user_input='m d testnumbers default q')
        assert score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnumbers')
        mpp = scoremanager.managers.MaterialPackageManager(
            'scoremanager.materialpackages.testnumbers')
        assert mpp.is_data_only
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        score_manager._run(pending_user_input='m testnumbers del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_02():
    r'''Make data package. Invalidate initializer.
    Verify invalid initializer. Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanager.materialpackages.testnumbers')

    try:
        score_manager._run(pending_user_input=
            'm d testnumbers default '
            'testnumbers incanned canned_exception.py default q')
        assert score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnumbers')
        mpp = scoremanager.managers.MaterialPackageManager(
            'scoremanager.materialpackages.testnumbers')
        assert mpp.is_data_only
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        score_manager._run(pending_user_input='m testnumbers del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_03():
    r'''Make data package. Corrupt initializer. Restore initializer.
    Verify initializer. Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanager.materialpackages.testnumbers')

    try:
        score_manager._run(pending_user_input=
            'm d testnumbers default '
            'testnumbers incanned canned_exception.py default '
            'inr yes no default q')
        assert score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnumbers')
        mpp = scoremanager.managers.MaterialPackageManager(
            'scoremanager.materialpackages.testnumbers')
        assert mpp.is_data_only
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        score_manager._run(pending_user_input='m testnumbers del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_04():
    r'''Make data package. Create output material.
    Delete package."
    '''

    score_manager = scoremanager.core.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanager.materialpackages.testnumbers')

    try:
        score_manager._run(pending_user_input=
            'm d testnumbers default '
            'testnumbers mdcanned canned_testnumbers_material_definition.py default '
            'omm default q')
        assert score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnumbers')
        mpp = scoremanager.managers.MaterialPackageManager(
            'scoremanager.materialpackages.testnumbers')
        assert mpp.is_data_only
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            'output_material.py', 
            ]
        assert mpp.material_definition == [1, 2, 3, 4, 5]
        assert mpp.output_material == [1, 2, 3, 4, 5]
    finally:
        score_manager._run(pending_user_input='m testnumbers del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_05():
    r'''Make data package. Delete material definition module.
    Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanager.materialpackages.testnumbers')

    try:
        score_manager._run(pending_user_input=
            'm d testnumbers default '
            'testnumbers mddelete default q')
        assert score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnumbers')
        mpp = scoremanager.managers.MaterialPackageManager(
            'scoremanager.materialpackages.testnumbers')
        assert mpp.is_data_only
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            ]
        assert not mpp.has_material_definition_module
        assert not mpp.has_output_material_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        score_manager._run(pending_user_input='m testnumbers del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_06():
    r'''Make data package. Overwrite material definition module with stub.
    Delete package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanager.materialpackages.testnumbers')

    try:
        score_manager._run(pending_user_input=
            'm d testnumbers default '
            'testnumbers mdstub default q')
        assert score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnumbers')
        mpp = scoremanager.managers.MaterialPackageManager(
            'scoremanager.materialpackages.testnumbers')
        assert mpp.is_data_only
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        score_manager._run(pending_user_input='m testnumbers del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_07():
    r'''Make data package. Copy canned material definition. 
    Make output material. Remove output material. Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanager.materialpackages.testnumbers')

    try:
        score_manager._run(pending_user_input=
            'm d testnumbers default '
            'testnumbers mdcanned canned_testnumbers_material_definition.py '
            'default '
            'omm default '
            'omdelete default q')
        assert score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnumbers')
        mpp = scoremanager.managers.MaterialPackageManager(
            'scoremanager.materialpackages.testnumbers')
        assert mpp.is_data_only
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert mpp.material_definition == [1, 2, 3, 4, 5]
        assert mpp.output_material is None
    finally:
        score_manager._run(
            pending_user_input='m testnumbers del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_08():
    r'''Make data package. Copy canned material definition with exception.
    Examine package state. Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanager.materialpackages.testnumbers')

    try:
        score_manager._run(pending_user_input=
            'm d testnumbers default '
            'testnumbers mdcanned canned_testnumbers_material_definition_with_exception.py default q')
        assert score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnumbers')
        mpp = scoremanager.managers.MaterialPackageManager(
            'scoremanager.materialpackages.testnumbers')
        assert mpp.is_data_only
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        score_manager._run(pending_user_input='m testnumbers del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnumbers')


def test_MaterialPackageWrangler_run_data_only_package_09():
    r'''Make data package. Copy canned material definition module. Make output data. Corrupt output data.
    Verify invalid output material module. Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanager.materialpackages.testnumbers')

    try:
        score_manager._run(pending_user_input=
            'm d testnumbers default '
            'testnumbers mdcanned canned_testnumbers_material_definition.py default '
            'omm default '
            'omcanned canned_exception.py default q')
        assert score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnumbers')
        mpp = scoremanager.managers.MaterialPackageManager(
            'scoremanager.materialpackages.testnumbers')
        assert mpp.is_data_only
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            'output_material.py', 
            ]
        assert mpp.material_definition == [1, 2, 3, 4, 5]
        assert mpp.output_material is None
    finally:
        score_manager._run(pending_user_input='m testnumbers del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testnumbers')
