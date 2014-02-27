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
#
#
#def test_MaterialPackageWrangler_run_managermade_package_04():
#    r'''Make managermade package. Corrupt initializer. Restore initializer.
#    Verify initializer. Remove package.
#    '''
#
#    score_manager = scoremanager.core.ScoreManager()
#    assert not score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'm nmm testsargasso default default '
#            'testsargasso incanned boilerplate_exception.py default '
#            'inr yes yes default q')
#        assert score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#        manager = scoremanager.managers.SargassoMeasureMaterialManager('scoremanager.materials.testsargasso')
#        assert manager._list_directory() == ['__init__.py', 'material_definition.py']
#        assert not manager.has_output_material_module
#        assert not os.path.isfile(manager.illustration_builder_module_path)
#        assert manager.material_definition is None
#        assert manager.output_material is None
#    finally:
#        score_manager._run(pending_user_input='m testsargasso rm default q')
#        assert not score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_managermade_package_05():
#    r'''Make managermade package. Create output material.
#    Delete package."
#    '''
#
#    score_manager = scoremanager.core.ScoreManager()
#    assert not score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'lmm nmm testsargasso default default '
#            'testsargasso mdbp boilerplate_testsargasso_material_definition.py default '
#            'omm default q')
#        assert score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#        manager = scoremanager.managers.SargassoMeasureMaterialManager('scoremanager.materials.testsargasso')
#        assert manager._list_directory() == ['__init__.py',
#            'illustration_builder.py', 'material_definition.py', 'output_material.py']
#        assert os.path.isfile(manager.illustration_builder_module_path)
#        assert manager.material_definition and all(isinstance(x, Note) for x in
#           manager.material_definition)
#        assert manager.output_material and and all(isinstance(x, Note) for x in
#           manager.output_material)
#    finally:
#        score_manager._run(pending_user_input='lmm testsargasso rm default q')
#        assert not score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_managermade_package_06():
#    r'''Make managermade package. Delete material definition module.
#    Remove package.
#    '''
#
#    score_manager = scoremanager.core.ScoreManager()
#    assert not score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'lmm nmm testsargasso default default '
#            'testsargasso mdrm default q')
#        assert score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#        manager = scoremanager.managers.SargassoMeasureMaterialManager('scoremanager.materials.testsargasso')
#        assert manager._list_directory() == ['__init__.py']
#        assert not manager.has_material_definition_module
#        assert not manager.has_output_material_module
#        assert not os.path.isfile(manager.illustration_builder_module_path)
#        assert manager.material_definition is None
#        assert manager.output_material is None
#    finally:
#        score_manager._run(pending_user_input='lmm testsargasso rm default q')
#        assert not score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_managermade_package_07():
#    r'''Make managermade package. Overwrite material definition module with stub.
#    Delete package.
#    '''
#
#    score_manager = scoremanager.core.ScoreManager()
#    assert not score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'lmm nmm testsargasso default default '
#            'testsargasso mds default q')
#        assert score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#        manager = scoremanager.managers.SargassoMeasureMaterialManager('scoremanager.materials.testsargasso')
#        assert manager._list_directory() == ['__init__.py', 'material_definition.py']
#        assert not manager.has_output_material_module
#        assert not os.path.isfile(manager.illustration_builder_module_path)
#        assert manager.material_definition is None
#        assert manager.output_material is None
#    finally:
#        score_manager._run(pending_user_input='lmm testsargasso rm default q')
#        assert not score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_managermade_package_08():
#    r'''Make managermade package. Copy canned material definition. Make output material. Remove output material.
#    Remove package.
#    '''
#
#    score_manager = scoremanager.core.ScoreManager()
#    assert not score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'lmm nmm testsargasso default default '
#            'testsargasso mdbp boilerplate_testsargasso_material_definition.py default '
#            'omm default '
#            'omrm default q')
#        assert score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#        manager = scoremanager.managers.SargassoMeasureMaterialManager('scoremanager.materials.testsargasso')
#        assert manager._list_directory() == ['__init__.py', 'material_definition.py']
#        assert not manager.has_output_material_module
#        assert not os.path.isfile(manager.illustration_builder_module_path)
#        assert manager.material_definition and all(isinstance(x, Note) for x in
#           manager.material_definition
#        assert manager.output_material is None
#    finally:
#        score_manager._run(pending_user_input='lmm testsargasso rm default q')
#        assert not score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_managermade_package_09():
#    r'''Make managermade package. Copy canned material definition with exception.
#    Examine package state. Remove package.
#    '''
#
#    score_manager = scoremanager.core.ScoreManager()
#    assert not score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'lmm nmm testsargasso default default '
#            'testsargasso mdbp boilerplate_exception.py default q')
#        assert score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#        manager = scoremanager.managers.SargassoMeasureMaterialManager('scoremanager.materials.testsargasso')
#        assert manager._list_directory() == ['__init__.py', 'material_definition.py']
#        assert not manager.has_output_material_module
#        assert not os.path.isfile(manager.illustration_builder_module_path)
#        assert manager.material_definition is None
#        assert manager.output_material is None
#    finally:
#        score_manager._run(pending_user_input='lmm testsargasso rm default q')
#        assert not score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_managermade_package_10():
#    r'''Make managermade package. Copy canned material definition module. Make output data. Corrupt output data.
#    Verify invalid output material module. Remove package.
#    '''
#
#    score_manager = scoremanager.core.ScoreManager()
#    assert not score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'lmm nmm testsargasso default default '
#            'testsargasso mdbp boilerplate_testsargasso_material_definition.py default '
#            'omm default '
#            'ombp boilerplate_exception.py default q')
#        assert score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#        manager = scoremanager.managers.SargassoMeasureMaterialManager('scoremanager.materials.testsargasso')
#        assert manager._list_directory() == ['__init__.py',
#            'illustration_builder.py', 'material_definition.py', 'output_material.py']
#        assert os.path.isfile(manager.illustration_builder_module_path)
#        assert manager.material_definition and all(isinstance(x, Note) for x in
#           manager.material_definition
#        assert manager.output_material is None
#    finally:
#        score_manager._run(pending_user_input='lmm testsargasso rm default q')
#        assert not score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_managermade_package_11():
#    r'''Make managermade package. Copy canned material definition module.
#    Make output data. Make PDF. Remove package.
#    '''
#
#    score_manager = scoremanager.core.ScoreManager()
#    assert not score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'lmm nmm testsargasso default default '
#            'testsargasso mdbp boilerplate_testsargasso_material_definition.py default '
#            'omm default '
#            'pdfm default '
#            'q')
#        assert score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
#        manager = scoremanager.managers.SargassoMeasureMaterialManager('scoremanager.materials.testsargasso')
#        assert manager._list_directory() == [
#            '__init__.py', 'illustration.ly', 'illustration.pdf',
#            'illustration_builder.py', 'material_definition.py', 'output_material.py']
#        assert manager.material_definition and all(isinstance(x, Note) for x in
#           manager.material_definition)
#        assert manager.output_material and all(isinstance(x, Note) for x in
#           manager.output_material
#    finally:
#        score_manager._run(pending_user_input='lmm testsargasso rm default q')
#        assert not score_manager._configuration.package_exists('scoremanager.materials.testsargasso')
