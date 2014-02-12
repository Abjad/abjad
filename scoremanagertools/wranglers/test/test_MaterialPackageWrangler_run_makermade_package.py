# -*- encoding: utf-8 -*-
import pytest
from experimental import *


def test_MaterialPackageWrangler_run_makermade_package_01():
    r'''Make makermade package. Delete package.
    '''

    score_manager = scoremanagertools.core.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')

    try:
        score_manager._run(pending_user_input='m m sargasso testsargasso default q')
        assert score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker(
            'scoremanagertools.materialpackages.testsargasso')
        assert mpp.is_makermade
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        assert mpp.has_initializer
        assert not mpp.has_output_material_module
        assert mpp.has_user_input_module
        assert mpp.output_material is None
    finally:
        score_manager._run(pending_user_input='m testsargasso del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')


def test_MaterialPackageWrangler_run_makermade_package_02():
    r'''Make score-resident makermade package. Delete package.
    '''

    score_manager = scoremanagertools.core.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanagertools.scorepackages.red_example_score.materials.testsargasso')

    try:
        score_manager._run(pending_user_input='red~example~score m m sargasso testsargasso default q')
        assert score_manager.configuration.packagesystem_path_exists(
            'scoremanagertools.scorepackages.red_example_score.materials.testsargasso')
        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker(
            'scoremanagertools.scorepackages.red_example_score.materials.testsargasso')
        assert mpp.is_makermade
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        assert mpp.has_initializer
        assert not mpp.has_output_material_module
        assert mpp.has_user_input_module
        assert mpp.output_material is None
    finally:
        score_manager._run(pending_user_input='red~example~score m testsargasso del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanagertools.scorepackages.red_example_score.materials.testsargasso')


#def test_MaterialPackageWrangler_run_makermade_package_03():
#    r'''Make makermade package. Corrupt initializer.
#    Verify invalid initializer. Remove package.
#    '''
#
#    score_manager = scoremanagertools.core.ScoreManager()
#    assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'm m testsargasso default default '
#            'testsargasso incanned canned_exception.py default q')
#        assert score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker('scoremanagertools.materialpackages.testsargasso')
#        assert mpp.is_makermade and not mpp.is_data_only
#        assert mpp._list_directory() == ['__init__.py', 'material_definition.py']
#        assert not mpp.has_output_material_module
#        assert not mpp.has_illustration_builder_module
#        assert mpp.material_definition is None
#        assert mpp.output_material is None
#        assert mpp.illustration is None
#    finally:
#        score_manager._run(pending_user_input='m testsargasso del remove default q')
#        assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_makermade_package_04():
#    r'''Make makermade package. Corrupt initializer. Restore initializer.
#    Verify initializer. Remove package.
#    '''
#
#    score_manager = scoremanagertools.core.ScoreManager()
#    assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'm m testsargasso default default '
#            'testsargasso incanned canned_exception.py default '
#            'inr yes yes default q')
#        assert score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker('scoremanagertools.materialpackages.testsargasso')
#        assert mpp.is_makermade and not mpp.is_data_only
#        assert mpp._list_directory() == ['__init__.py', 'material_definition.py']
#        assert not mpp.has_output_material_module
#        assert not mpp.has_illustration_builder_module
#        assert mpp.material_definition is None
#        assert mpp.output_material is None
#    finally:
#        score_manager._run(pending_user_input='m testsargasso del remove default q')
#        assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_makermade_package_05():
#    r'''Make makermade package. Create output material.
#    Delete package."
#    '''
#
#    score_manager = scoremanagertools.core.ScoreManager()
#    assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'm m testsargasso default default '
#            'testsargasso mdcanned canned_testsargasso_material_definition.py default '
#            'omm default q')
#        assert score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker('scoremanagertools.materialpackages.testsargasso')
#        assert mpp.is_makermade and not mpp.is_data_only
#        assert mpp._list_directory() == ['__init__.py',
#            'illustration_builder.py', 'material_definition.py', 'output_material.py']
#        assert mpp.has_illustration_builder_module
#        assert mpp.material_definition and all(isinstance(x, Note) for x in
#           mpp.material_definition)
#        assert mpp.output_material and and all(isinstance(x, Note) for x in
#           mpp.output_material)
#    finally:
#        score_manager._run(pending_user_input='m testsargasso del remove default q')
#        assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_makermade_package_06():
#    r'''Make makermade package. Delete material definition module.
#    Remove package.
#    '''
#
#    score_manager = scoremanagertools.core.ScoreManager()
#    assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'm m testsargasso default default '
#            'testsargasso mddelete default q')
#        assert score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker('scoremanagertools.materialpackages.testsargasso')
#        assert mpp.is_makermade and not mpp.is_data_only
#        assert mpp._list_directory() == ['__init__.py']
#        assert not mpp.has_material_definition_module
#        assert not mpp.has_output_material_module
#        assert not mpp.has_illustration_builder_module
#        assert mpp.material_definition is None
#        assert mpp.output_material is None
#    finally:
#        score_manager._run(pending_user_input='m testsargasso del remove default q')
#        assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_makermade_package_07():
#    r'''Make makermade package. Overwrite material definition module with stub.
#    Delete package.
#    '''
#
#    score_manager = scoremanagertools.core.ScoreManager()
#    assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'm m testsargasso default default '
#            'testsargasso mdstub default q')
#        assert score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker('scoremanagertools.materialpackages.testsargasso')
#        assert mpp.is_makermade and not mpp.is_data_only
#        assert mpp._list_directory() == ['__init__.py', 'material_definition.py']
#        assert not mpp.has_output_material_module
#        assert not mpp.has_illustration_builder_module
#        assert mpp.material_definition is None
#        assert mpp.output_material is None
#    finally:
#        score_manager._run(pending_user_input='m testsargasso del remove default q')
#        assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_makermade_package_08():
#    r'''Make makermade package. Copy canned material definition. Make output material. Remove output material.
#    Remove package.
#    '''
#
#    score_manager = scoremanagertools.core.ScoreManager()
#    assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'm m testsargasso default default '
#            'testsargasso mdcanned canned_testsargasso_material_definition.py default '
#            'omm default '
#            'omdelete default q')
#        assert score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker('scoremanagertools.materialpackages.testsargasso')
#        assert mpp.is_makermade and not mpp.is_data_only
#        assert mpp._list_directory() == ['__init__.py', 'material_definition.py']
#        assert not mpp.has_output_material_module
#        assert not mpp.has_illustration_builder_module
#        assert mpp.material_definition and all(isinstance(x, Note) for x in
#           mpp.material_definition
#        assert mpp.output_material is None
#    finally:
#        score_manager._run(pending_user_input='m testsargasso del remove default q')
#        assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_makermade_package_09():
#    r'''Make makermade package. Copy canned material definition with exception.
#    Examine package state. Remove package.
#    '''
#
#    score_manager = scoremanagertools.core.ScoreManager()
#    assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'm m testsargasso default default '
#            'testsargasso mdcanned canned_exception.py default q')
#        assert score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker('scoremanagertools.materialpackages.testsargasso')
#        assert mpp.is_makermade and not mpp.is_data_only
#        assert mpp._list_directory() == ['__init__.py', 'material_definition.py']
#        assert not mpp.has_output_material_module
#        assert not mpp.has_illustration_builder_module
#        assert mpp.material_definition is None
#        assert mpp.output_material is None
#    finally:
#        score_manager._run(pending_user_input='m testsargasso del remove default q')
#        assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_makermade_package_10():
#    r'''Make makermade package. Copy canned material definition module. Make output data. Corrupt output data.
#    Verify invalid output material module. Remove package.
#    '''
#
#    score_manager = scoremanagertools.core.ScoreManager()
#    assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'm m testsargasso default default '
#            'testsargasso mdcanned canned_testsargasso_material_definition.py default '
#            'omm default '
#            'omcanned canned_exception.py default q')
#        assert score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker('scoremanagertools.materialpackages.testsargasso')
#        assert mpp.is_makermade and not mpp.is_data_only
#        assert mpp._list_directory() == ['__init__.py',
#            'illustration_builder.py', 'material_definition.py', 'output_material.py']
#        assert mpp.has_illustration_builder_module
#        assert mpp.material_definition and all(isinstance(x, Note) for x in
#           mpp.material_definition
#        assert mpp.output_material is None
#    finally:
#        score_manager._run(pending_user_input='m testsargasso del remove default q')
#        assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#
#
#def test_MaterialPackageWrangler_run_makermade_package_11():
#    r'''Make makermade package. Copy canned material definition module.
#    Make output data. Make PDF. Remove package.
#    '''
#
#    score_manager = scoremanagertools.core.ScoreManager()
#    assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#
#    try:
#        score_manager._run(pending_user_input=
#            'm m testsargasso default default '
#            'testsargasso mdcanned canned_testsargasso_material_definition.py default '
#            'omm default '
#            'pdfm default '
#            'q')
#        assert score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
#        mpp = scoremanagertools.materialpackagemakers.SargassoMeasureMaterialPackageMaker('scoremanagertools.materialpackages.testsargasso')
#        assert mpp.is_makermade and not mpp.is_data_only
#        assert mpp._list_directory() == [
#            '__init__.py', 'illustration.ly', 'illustration.pdf',
#            'illustration_builder.py', 'material_definition.py', 'output_material.py']
#        assert mpp.has_illustration_ly
#        assert mpp.has_illustration_pdf
#        assert mpp.material_definition and all(isinstance(x, Note) for x in
#           mpp.material_definition)
#        assert mpp.output_material and all(isinstance(x, Note) for x in
#           mpp.output_material
#    finally:
#        score_manager._run(pending_user_input='m testsargasso del remove default q')
#        assert not score_manager.configuration.packagesystem_path_exists('scoremanagertools.materialpackages.testsargasso')
