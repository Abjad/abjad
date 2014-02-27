# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_run_managermade_package_01():
    r'''Make managermade package. Delete package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    name = 'scoremanager.materials.testsargasso'
    assert not score_manager._configuration.package_exists(name)
    filesystem_path = os.path.join(
        score_manager._configuration.abjad_material_packages_directory_path,
        'testsargasso',
        )

    try:
        string = 'lmm nmm sargasso testsargasso default q'
        score_manager._run(pending_user_input=string)
        assert score_manager._configuration.package_exists(name)
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            filesystem_path=filesystem_path)
        assert manager._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        assert os.path.isfile(manager._initializer_file_path)
        assert not manager.has_output_material_module
        assert manager.has_user_input_module
        assert manager.output_material is None
    finally:
        string = 'lmm testsargasso rm default q'
        score_manager._run(pending_user_input=string)
        assert not score_manager._configuration.package_exists(name)


def test_MaterialPackageWrangler_run_managermade_package_02():
    r'''Make score-resident managermade package. Delete package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    name = 'scoremanager.scores.red_example_score.materials.testsargasso'
    assert not score_manager._configuration.package_exists(name)
    filesystem_path = os.path.join(
        score_manager._configuration.abjad_score_packages_directory_path,
        'red_example_score',
        'materials',
        'testsargasso',
        )

    try:
        string = 'red~example~score m nmm sargasso testsargasso default q'
        score_manager._run(pending_user_input=string)
        assert score_manager._configuration.package_exists(name)
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            filesystem_path=filesystem_path)
        assert manager._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        assert os.path.isfile(manager._initializer_file_path)
        assert not manager.has_output_material_module
        assert manager.has_user_input_module
        assert manager.output_material is None
    finally:
        string = 'red~example~score m testsargasso rm default q'
        score_manager._run(pending_user_input='red~example~score m testsargasso rm default q')
        assert not score_manager._configuration.package_exists(name)


#def test_MaterialPackageWrangler_run_managermade_package_03():
#    r'''Make managermade package. Corrupt initializer.
#    Verify invalid initializer. Remove package.
#    '''
#
#    score_manager = scoremanager.core.ScoreManager()
#    assert not score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'm nmm testsargasso default default '
#            'testsargasso incanned boilerplate_exception.py default q')
#        assert score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#        manager = scoremanager.managers.SargassoMeasureMaterialManager('scoremanager.materials.testsargasso')
#        assert manager._list_directory() == ['__init__.py', 'material_definition.py']
#        assert not manager.has_output_material_module
#        assert not os.path.isfile(manager.illustration_builder_module_path)
#        assert manager.material_definition is None
#        assert manager.output_material is None
#        assert manager.illustration is None
#    finally:
#        score_manager._run(pending_user_input='m testsargasso rm default q')
#        assert not score_manager._configuration.package_exists('scoremanager.materials.testsargasso')


def test_MaterialPackageWrangler_run_managermade_package_04():
    r'''Make managermade package. Corrupt initializer. Restore initializer.
    Verify initializer. Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    package = 'scoremanager.materials.testsargassomeasures'
    assert not score_manager._configuration.package_exists(package)
    filesystem_path = os.path.join(
        score_manager._configuration.abjad_material_packages_directory_path,
        'testsargassomeasures',
        )
    input_ = 'lmm nmm sargasso testsargassomeasures'
    input_ += ' omi inbp boilerplate_exception.py default'
    input_ += ' ins default q'
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'user_input.py',
        ]

    try:
        score_manager._run(pending_user_input=input_)
        assert score_manager._configuration.package_exists(package)
        manager = scoremanager.managers.SargassoMeasureMaterialManager(
            filesystem_path=filesystem_path)
        assert manager._list_directory() == directory_entries
        assert not manager.has_output_material_module
        assert not os.path.isfile(manager.illustration_builder_module_path)
        assert manager.material_definition is None
        assert manager.output_material is None
    finally:
        input_ = 'lmm testsargassomeasures rm default q'
        score_manager._run(pending_user_input=input_)
        assert not score_manager._configuration.package_exists(package)
