# -*- encoding: utf-8 -*-
from experimental import *
import py


def test_MaterialPackageWrangler_run_handmade_package_01():
    r'''Make handmade package. Delete package.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')

    try:
        score_manager._run(pending_user_input='m h testnotes default default q')
        assert score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')
        mpp = scoremanagertools.proxies.MaterialPackageManager('experimental.tools.scoremanagertools.materialpackages.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        score_manager._run(pending_user_input='m testnotes del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')


def test_MaterialPackageWrangler_run_handmade_package_02():
    r'''Make handmade package. Corrupt initializer.
    Verify invalid initializer. Remove package.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')

    try:
        score_manager._run(pending_user_input=
            'm h testnotes default default '
            'testnotes incanned canned_exception.py default q')
        assert score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')
        mpp = scoremanagertools.proxies.MaterialPackageManager('experimental.tools.scoremanagertools.materialpackages.testnotes')
        assert mpp.list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        score_manager._run(pending_user_input='m testnotes del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')


def test_MaterialPackageWrangler_run_handmade_package_03():
    r'''Make handmade package. Corrupt initializer. Restore initializer.
    Verify initializer. Remove package.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')

    try:
        score_manager._run(pending_user_input=
            'm h testnotes default default '
            'testnotes incanned canned_exception.py default '
            'inr yes yes default q')
        assert score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')
        mpp = scoremanagertools.proxies.MaterialPackageManager('experimental.tools.scoremanagertools.materialpackages.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        score_manager._run(pending_user_input='m testnotes del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')


def test_MaterialPackageWrangler_run_handmade_package_04():
    r'''Make handmade package. Create output material.
    Delete package."
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')

    try:
        score_manager._run(pending_user_input=
            'm h testnotes default default '
            'testnotes mdcanned canned_testnotes_material_definition.py default '
            'omm default q')
        assert score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')
        mpp = scoremanagertools.proxies.MaterialPackageManager('experimental.tools.scoremanagertools.materialpackages.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.list_directory() == [
            '__init__.py',
            '__metadata__.py',
            'illustration_builder.py', 
            'material_definition.py', 
            'output_material.py', 
            ]
        assert mpp.has_user_finalized_material_definition_module
        assert mpp.has_illustration_builder_module
        assert mpp.material_definition and \
            all(isinstance(x, Note) for x in mpp.material_definition)
        assert mpp.output_material and \
            all(isinstance(x, Note) for x in mpp.output_material)
    finally:
        score_manager._run(pending_user_input='m testnotes del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')


def test_MaterialPackageWrangler_run_handmade_package_05():
    r'''Make handmade package. Delete material definition module.
    Remove package.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')

    try:
        score_manager._run(pending_user_input=
            'm h testnotes default default '
            'testnotes mddelete default q')
        assert score_manager.configuration.packagesystem_path_exists(
            'experimental.tools.scoremanagertools.materialpackages.testnotes')
        mpp = scoremanagertools.proxies.MaterialPackageManager(
            'experimental.tools.scoremanagertools.materialpackages.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            ]
        assert not mpp.has_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        score_manager._run(
            pending_user_input='m testnotes del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'experimental.tools.scoremanagertools.materialpackages.testnotes')


def test_MaterialPackageWrangler_run_handmade_package_06():
    r'''Make handmade package. Overwrite material definition module with stub.
    Delete package.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')

    try:
        score_manager._run(pending_user_input=
            'm h testnotes default '
            'testnotes mdstub default q')
        assert score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')
        mpp = scoremanagertools.proxies.MaterialPackageManager('experimental.tools.scoremanagertools.materialpackages.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        score_manager._run(pending_user_input='m testnotes del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')


def test_MaterialPackageWrangler_run_handmade_package_07():
    r'''Make handmade package. Copy canned material definition. Make output material. Remove output material.
    Remove package.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')

    try:
        score_manager._run(pending_user_input=
            'm h testnotes default default '
            'testnotes mdcanned canned_testnotes_material_definition.py '
            'default '
            'omm default '
            'omdelete default q')
        assert score_manager.configuration.packagesystem_path_exists(
            'experimental.tools.scoremanagertools.materialpackages.testnotes')
        mpp = scoremanagertools.proxies.MaterialPackageManager(
            'experimental.tools.scoremanagertools.materialpackages.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.list_directory() == [
                '__init__.py', 
                '__metadata__.py',
                'material_definition.py', 
                ]
        assert mpp.has_user_finalized_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert mpp.material_definition and \
            all(isinstance(x, Note) for x in mpp.material_definition)
        assert mpp.output_material is None
    finally:
        score_manager._run(
            pending_user_input='m testnotes del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'experimental.tools.scoremanagertools.materialpackages.testnotes')


def test_MaterialPackageWrangler_run_handmade_package_08():
    r'''Make handmade package. Copy canned material definition with exception.
    Examine package state. Remove package.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')

    try:
        score_manager._run(pending_user_input=
            'm h testnotes default default '
            'testnotes mdcanned canned_exception.py default q')
        assert score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')
        mpp = scoremanagertools.proxies.MaterialPackageManager('experimental.tools.scoremanagertools.materialpackages.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        score_manager._run(pending_user_input='m testnotes del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')


def test_MaterialPackageWrangler_run_handmade_package_09():
    r'''Make handmade package. Copy canned material definition module. Make output data. Corrupt output data.
    Verify invalid output material module. Remove package.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')

    try:
        score_manager._run(pending_user_input=
            'm h testnotes default default '
            'testnotes mdcanned canned_testnotes_material_definition.py default '
            'omm default '
            'omcanned canned_exception.py default q')
        assert score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')
        mpp = scoremanagertools.proxies.MaterialPackageManager('experimental.tools.scoremanagertools.materialpackages.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.list_directory() == [
            '__init__.py',
            '__metadata__.py',
            'illustration_builder.py', 
            'material_definition.py', 
            'output_material.py', 
            ]
        assert mpp.has_user_finalized_material_definition_module
        assert mpp.has_illustration_builder_module
        assert mpp.material_definition and \
            all(isinstance(x, Note) for x in mpp.material_definition)
        assert mpp.output_material is None
    finally:
        score_manager._run(pending_user_input='m testnotes del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')


def test_MaterialPackageWrangler_run_handmade_package_10():
    r'''Make handmade package. Copy canned material definition module.
    Make output data. Make PDF. Remove package.
    '''
    py.test.skip('skip this one during day-to-day development and before build only.')

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')

    try:
        score_manager._run(pending_user_input=
            'm h testnotes default default '
            'testnotes mdcanned canned_testnotes_material_definition.py default '
            'omm default '
            'pdfm default '
            'q')
        assert score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')
        mpp = scoremanagertools.proxies.MaterialPackageManager('experimental.tools.scoremanagertools.materialpackages.testnotes')
        assert mpp.is_handmade and not mpp.is_data_only
        assert mpp.list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'illustration.ly', 
            'illustration.pdf',
            'illustration_builder.py', 
            'material_definition.py', 
            'output_material.py', 
            ]
        assert mpp.has_user_finalized_material_definition_module
        assert mpp.has_user_finalized_illustration_builder_module
        assert mpp.has_illustration_ly
        assert mpp.has_illustration_pdf
        assert mpp.material_definition and \
            all(isinstance(x, Note) for x in mpp.material_definition)
        assert mpp.output_material and \
            all(isinstance(x, Note) for x in mpp.output_material)
            
    finally:
        score_manager._run(pending_user_input='m testnotes del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists('experimental.tools.scoremanagertools.materialpackages.testnotes')
