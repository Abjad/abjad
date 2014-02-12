# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_make_makermade_material_package_01():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.testsargasso'
    assert not wrangler.configuration.packagesystem_path_exists(string)

    try:
        wrangler.make_makermade_material_package(
            string, 
            'SargassoMeasureMaterialPackageMaker',
            )
        assert wrangler.configuration.packagesystem_path_exists(string)
        mpp = scoremanager.materialpackagemakers.SargassoMeasureMaterialPackageMaker(string)
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
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists(string)


def test_MaterialPackageWrangler_make_makermade_material_package_02():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.red_numbers'
    assert wrangler.configuration.packagesystem_path_exists(string)
    statement = "wrangler.make_makermade_material_package("
    statement += "'scoremanager.materialpackages.red_sargasso_measures"
    statement += "'SargassoMeasureMaterialPackageMaker')"
    assert pytest.raises(Exception, statement)


def test_MaterialPackageWrangler_make_makermade_material_package_03():
    r'''Interactively.
    '''

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.testsargasso'
    assert not wrangler.configuration.packagesystem_path_exists(string)

    try:
        wrangler.interactively_make_makermade_material_package(
            pending_user_input='sargasso testsargasso q')
        assert wrangler.configuration.packagesystem_path_exists(string)
        mpp = scoremanager.materialpackagemakers.SargassoMeasureMaterialPackageMaker(string)
        assert mpp.is_makermade
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists(string)


def test_MaterialPackageWrangler_make_makermade_material_package_04():

    wrangler = scoremanager.wranglers.MaterialPackageWrangler()
    string = 'scoremanager.materialpackages.testsargasso'
    assert not wrangler.configuration.packagesystem_path_exists(string)

    try:
        tags = {'color': 'red', 'is_colored': True}
        wrangler.make_makermade_material_package(
            string, 
            'SargassoMeasureMaterialPackageMaker', 
            tags=tags,
            )
        assert wrangler.configuration.packagesystem_path_exists(string)
        mpp = scoremanager.materialpackagemakers.SargassoMeasureMaterialPackageMaker(string)
        assert mpp.is_makermade
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'user_input.py',
            ]
        assert mpp._get_metadata('color') == 'red'
        assert mpp._get_metadata('is_colored')
    finally:
        mpp.remove()
        assert not wrangler.configuration.packagesystem_path_exists(string)
