# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_run_managermade_package_01():
    r'''Make managermade package. Delete package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    name = 'scoremanager.materialpackages.testsargasso'
    assert not score_manager._configuration.package_exists(name)

    try:
        string = 'lmm nmm sargasso testsargasso default q'
        score_manager._run(pending_user_input=string)
        assert score_manager._configuration.package_exists(name)
        manager = scoremanager.materialpackagemanagers.SargassoMeasureMaterialPackageManager(name)
        assert manager.is_managermade
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
        string = 'lmm testsargasso del remove default q'
        score_manager._run(pending_user_input=string)
        assert not score_manager._configuration.package_exists(name)


def test_MaterialPackageWrangler_run_managermade_package_02():
    r'''Make score-resident managermade package. Delete package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    name = 'scoremanager.scorepackages.red_example_score.materials.testsargasso'
    assert not score_manager._configuration.package_exists(name)

    try:
        string = 'red~example~score m nmm sargasso testsargasso default q'
        score_manager._run(pending_user_input=string)
        assert score_manager._configuration.package_exists(name)
        manager = scoremanager.materialpackagemanagers.SargassoMeasureMaterialPackageManager(name)
        assert manager.is_managermade
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
        string = 'red~example~score m testsargasso del remove default q'
        score_manager._run(pending_user_input='red~example~score m testsargasso del remove default q')
        assert not score_manager._configuration.package_exists(name)


#def test_MaterialPackageWrangler_run_managermade_package_03():
#    r'''Make managermade package. Corrupt initializer.
#    Verify invalid initializer. Remove package.
#    '''
#
#    score_manager = scoremanager.core.ScoreManager()
#    assert not score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'm nmm testsargasso default default '
#            'testsargasso incanned boilerplate_exception.py default q')
#        assert score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#        manager = scoremanager.materialpackagemanagers.SargassoMeasureMaterialPackageManager('scoremanager.materialpackages.testsargasso')
#        assert manager._list_directory() == ['__init__.py', 'material_definition.py']
#        assert not manager.has_output_material_module
#        assert not manager.has_illustration_builder_module
#        assert manager.material_definition is None
#        assert manager.output_material is None
#        assert manager.illustration is None
#    finally:
#        score_manager._run(pending_user_input='m testsargasso del remove default q')
#        assert not score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_managermade_package_04():
#    r'''Make managermade package. Corrupt initializer. Restore initializer.
#    Verify initializer. Remove package.
#    '''
#
#    score_manager = scoremanager.core.ScoreManager()
#    assert not score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'm nmm testsargasso default default '
#            'testsargasso incanned boilerplate_exception.py default '
#            'inr yes yes default q')
#        assert score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#        manager = scoremanager.materialpackagemanagers.SargassoMeasureMaterialPackageManager('scoremanager.materialpackages.testsargasso')
#        assert manager._list_directory() == ['__init__.py', 'material_definition.py']
#        assert not manager.has_output_material_module
#        assert not manager.has_illustration_builder_module
#        assert manager.material_definition is None
#        assert manager.output_material is None
#    finally:
#        score_manager._run(pending_user_input='m testsargasso del remove default q')
#        assert not score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_managermade_package_05():
#    r'''Make managermade package. Create output material.
#    Delete package."
#    '''
#
#    score_manager = scoremanager.core.ScoreManager()
#    assert not score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'lmm nmm testsargasso default default '
#            'testsargasso mdcanned boilerplate_testsargasso_material_definition.py default '
#            'omm default q')
#        assert score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#        manager = scoremanager.materialpackagemanagers.SargassoMeasureMaterialPackageManager('scoremanager.materialpackages.testsargasso')
#        assert manager._list_directory() == ['__init__.py',
#            'illustration_builder.py', 'material_definition.py', 'output_material.py']
#        assert manager.has_illustration_builder_module
#        assert manager.material_definition and all(isinstance(x, Note) for x in
#           manager.material_definition)
#        assert manager.output_material and and all(isinstance(x, Note) for x in
#           manager.output_material)
#    finally:
#        score_manager._run(pending_user_input='lmm testsargasso del remove default q')
#        assert not score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_managermade_package_06():
#    r'''Make managermade package. Delete material definition module.
#    Remove package.
#    '''
#
#    score_manager = scoremanager.core.ScoreManager()
#    assert not score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'lmm nmm testsargasso default default '
#            'testsargasso mddelete default q')
#        assert score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#        manager = scoremanager.materialpackagemanagers.SargassoMeasureMaterialPackageManager('scoremanager.materialpackages.testsargasso')
#        assert manager._list_directory() == ['__init__.py']
#        assert not manager.has_material_definition_module
#        assert not manager.has_output_material_module
#        assert not manager.has_illustration_builder_module
#        assert manager.material_definition is None
#        assert manager.output_material is None
#    finally:
#        score_manager._run(pending_user_input='lmm testsargasso del remove default q')
#        assert not score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_managermade_package_07():
#    r'''Make managermade package. Overwrite material definition module with stub.
#    Delete package.
#    '''
#
#    score_manager = scoremanager.core.ScoreManager()
#    assert not score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'lmm nmm testsargasso default default '
#            'testsargasso mdstub default q')
#        assert score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#        manager = scoremanager.materialpackagemanagers.SargassoMeasureMaterialPackageManager('scoremanager.materialpackages.testsargasso')
#        assert manager._list_directory() == ['__init__.py', 'material_definition.py']
#        assert not manager.has_output_material_module
#        assert not manager.has_illustration_builder_module
#        assert manager.material_definition is None
#        assert manager.output_material is None
#    finally:
#        score_manager._run(pending_user_input='lmm testsargasso del remove default q')
#        assert not score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_managermade_package_08():
#    r'''Make managermade package. Copy canned material definition. Make output material. Remove output material.
#    Remove package.
#    '''
#
#    score_manager = scoremanager.core.ScoreManager()
#    assert not score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'lmm nmm testsargasso default default '
#            'testsargasso mdcanned boilerplate_testsargasso_material_definition.py default '
#            'omm default '
#            'omdelete default q')
#        assert score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#        manager = scoremanager.materialpackagemanagers.SargassoMeasureMaterialPackageManager('scoremanager.materialpackages.testsargasso')
#        assert manager._list_directory() == ['__init__.py', 'material_definition.py']
#        assert not manager.has_output_material_module
#        assert not manager.has_illustration_builder_module
#        assert manager.material_definition and all(isinstance(x, Note) for x in
#           manager.material_definition
#        assert manager.output_material is None
#    finally:
#        score_manager._run(pending_user_input='lmm testsargasso del remove default q')
#        assert not score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_managermade_package_09():
#    r'''Make managermade package. Copy canned material definition with exception.
#    Examine package state. Remove package.
#    '''
#
#    score_manager = scoremanager.core.ScoreManager()
#    assert not score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'lmm nmm testsargasso default default '
#            'testsargasso mdcanned boilerplate_exception.py default q')
#        assert score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#        manager = scoremanager.materialpackagemanagers.SargassoMeasureMaterialPackageManager('scoremanager.materialpackages.testsargasso')
#        assert manager._list_directory() == ['__init__.py', 'material_definition.py']
#        assert not manager.has_output_material_module
#        assert not manager.has_illustration_builder_module
#        assert manager.material_definition is None
#        assert manager.output_material is None
#    finally:
#        score_manager._run(pending_user_input='lmm testsargasso del remove default q')
#        assert not score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_managermade_package_10():
#    r'''Make managermade package. Copy canned material definition module. Make output data. Corrupt output data.
#    Verify invalid output material module. Remove package.
#    '''
#
#    score_manager = scoremanager.core.ScoreManager()
#    assert not score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'lmm nmm testsargasso default default '
#            'testsargasso mdcanned boilerplate_testsargasso_material_definition.py default '
#            'omm default '
#            'omcanned boilerplate_exception.py default q')
#        assert score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#        manager = scoremanager.materialpackagemanagers.SargassoMeasureMaterialPackageManager('scoremanager.materialpackages.testsargasso')
#        assert manager._list_directory() == ['__init__.py',
#            'illustration_builder.py', 'material_definition.py', 'output_material.py']
#        assert manager.has_illustration_builder_module
#        assert manager.material_definition and all(isinstance(x, Note) for x in
#           manager.material_definition
#        assert manager.output_material is None
#    finally:
#        score_manager._run(pending_user_input='lmm testsargasso del remove default q')
#        assert not score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_managermade_package_11():
#    r'''Make managermade package. Copy canned material definition module.
#    Make output data. Make PDF. Remove package.
#    '''
#
#    score_manager = scoremanager.core.ScoreManager()
#    assert not score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'lmm nmm testsargasso default default '
#            'testsargasso mdcanned boilerplate_testsargasso_material_definition.py default '
#            'omm default '
#            'pdfm default '
#            'q')
#        assert score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
#        manager = scoremanager.materialpackagemanagers.SargassoMeasureMaterialPackageManager('scoremanager.materialpackages.testsargasso')
#        assert manager._list_directory() == [
#            '__init__.py', 'illustration.ly', 'illustration.pdf',
#            'illustration_builder.py', 'material_definition.py', 'output_material.py']
#        assert manager.has_illustration_ly
#        assert manager.has_illustration_pdf
#        assert manager.material_definition and all(isinstance(x, Note) for x in
#           manager.material_definition)
#        assert manager.output_material and all(isinstance(x, Note) for x in
#           manager.output_material
#    finally:
#        score_manager._run(pending_user_input='lmm testsargasso del remove default q')
#        assert not score_manager._configuration.package_exists('scoremanager.materialpackages.testsargasso')
