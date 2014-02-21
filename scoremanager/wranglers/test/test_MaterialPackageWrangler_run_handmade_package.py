# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_run_handmade_package_01():
    r'''Make handmade package. Delete package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    name = 'scoremanager.materialpackages.testnotes'
    assert not score_manager.configuration.package_path_exists(name)

    try:
        string = 'lmm nmh testnotes default default q'
        score_manager._run(pending_user_input=string)
        assert score_manager.configuration.package_path_exists(name)
        mpp = scoremanager.managers.MaterialPackageManager(name)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        string = 'lmm testnotes del remove default q'
        score_manager._run(pending_user_input=string)
        assert not score_manager.configuration.package_path_exists(name)


def test_MaterialPackageWrangler_run_handmade_package_02():
    r'''Make handmade package. Corrupt initializer.
    Verify invalid initializer. Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    name = 'scoremanager.materialpackages.testnotes'
    assert not score_manager.configuration.package_path_exists(name)

    try:
        score_manager._run(pending_user_input=
            'lmm nmh testnotes default default '
            'testnotes incanned boilerplate_exception.py default q')
        assert score_manager.configuration.package_path_exists(name)
        mpp = scoremanager.managers.MaterialPackageManager(name)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        string = 'lmm testnotes del remove default q'
        score_manager._run(pending_user_input=string)
        assert not score_manager.configuration.package_path_exists(name)


def test_MaterialPackageWrangler_run_handmade_package_03():
    r'''Make handmade package. Corrupt initializer. Restore initializer.
    Verify initializer. Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    name = 'scoremanager.materialpackages.testnotes'
    assert not score_manager.configuration.package_path_exists(name)

    try:
        score_manager._run(pending_user_input=
            'lmm nmh testnotes default default '
            'testnotes incanned boilerplate_exception.py default '
            'inr yes yes default q')
        assert score_manager.configuration.package_path_exists(name)
        mpp = scoremanager.managers.MaterialPackageManager(name)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        string = 'lmm testnotes del remove default q'
        score_manager._run(pending_user_input=string)
        assert not score_manager.configuration.package_path_exists(name)


def test_MaterialPackageWrangler_run_handmade_package_04():
    r'''Make handmade package. Create output material.
    Delete package."
    '''

    score_manager = scoremanager.core.ScoreManager()
    name = 'scoremanager.materialpackages.testnotes'
    assert not score_manager.configuration.package_path_exists(name)

    try:
        score_manager._run(pending_user_input=
            'lmm nmh testnotes default default '
            'testnotes mdcanned boilerplate_testnotes_material_definition.py default '
            'omm default q')
        assert score_manager.configuration.package_path_exists(name)
        mpp = scoremanager.managers.MaterialPackageManager(name)
        assert mpp._list_directory() == [
            '__init__.py',
            '__metadata__.py',
            'illustration_builder.py', 
            'material_definition.py', 
            'output_material.py', 
            ]
        assert mpp.has_illustration_builder_module
        assert mpp.material_definition and \
            all(isinstance(x, Note) for x in mpp.material_definition)
        assert mpp.output_material and \
            all(isinstance(x, Note) for x in mpp.output_material)
    finally:
        string = 'lmm testnotes del remove default q'
        score_manager._run(pending_user_input=string)
        assert not score_manager.configuration.package_path_exists(name)


def test_MaterialPackageWrangler_run_handmade_package_05():
    r'''Make handmade package. Delete material definition module.
    Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    name = 'scoremanager.materialpackages.testnotes'
    assert not score_manager.configuration.package_path_exists(name)

    try:
        score_manager._run(pending_user_input=
            'lmm nmh testnotes default default '
            'testnotes mddelete default q')
        assert score_manager.configuration.package_path_exists(name)
        mpp = scoremanager.managers.MaterialPackageManager(name)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            ]
        assert not mpp.has_material_definition_module
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        string = 'lmm testnotes del remove default q'
        score_manager._run(pending_user_input=string)
        assert not score_manager.configuration.package_path_exists(name)


def test_MaterialPackageWrangler_run_handmade_package_06():
    r'''Make handmade package. Overwrite material definition module with stub.
    Delete package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    name = 'scoremanager.materialpackages.testnotes'
    assert not score_manager.configuration.package_path_exists(name)

    try:
        score_manager._run(pending_user_input=
            'lmm nmh testnotes default '
            'testnotes mdstub default q')
        assert score_manager.configuration.package_path_exists(name)
        mpp = scoremanager.managers.MaterialPackageManager(name)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        string = 'lmm testnotes del remove default q'
        score_manager._run(pending_user_input=string)
        assert not score_manager.configuration.package_path_exists(name)


def test_MaterialPackageWrangler_run_handmade_package_07():
    r'''Make handmade package. Copy canned material definition. 
    Make output material. Remove output material. Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    name = 'scoremanager.materialpackages.testnotes'
    assert not score_manager.configuration.package_path_exists(name)

    try:
        score_manager._run(pending_user_input=
            'lmm nmh testnotes default default '
            'testnotes mdcanned boilerplate_testnotes_material_definition.py '
            'default '
            'omm default '
            'omdelete default q')
        assert score_manager.configuration.package_path_exists(name)
        mpp = scoremanager.managers.MaterialPackageManager(name)
        assert mpp._list_directory() == [
                '__init__.py', 
                '__metadata__.py',
                'material_definition.py', 
                ]
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert mpp.material_definition and \
            all(isinstance(x, Note) for x in mpp.material_definition)
        assert mpp.output_material is None
    finally:
        string = 'lmm testnotes del remove default q'
        score_manager._run(pending_user_input=string)
        assert not score_manager.configuration.package_path_exists(name)


def test_MaterialPackageWrangler_run_handmade_package_08():
    r'''Make handmade package. Copy canned material definition with exception.
    Examine package state. Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    name = 'scoremanager.materialpackages.testnotes'
    assert not score_manager.configuration.package_path_exists(name)

    try:
        score_manager._run(pending_user_input=
            'lmm nmh testnotes default default '
            'testnotes mdcanned boilerplate_exception.py default q')
        assert score_manager.configuration.package_path_exists(name)
        mpp = scoremanager.managers.MaterialPackageManager(name)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'material_definition.py', 
            ]
        assert not mpp.has_output_material_module
        assert not mpp.has_illustration_builder_module
        assert mpp.material_definition is None
        assert mpp.output_material is None
    finally:
        string = 'lmm testnotes del remove default q'
        score_manager._run(pending_user_input=string)
        assert not score_manager.configuration.package_path_exists(name)


def test_MaterialPackageWrangler_run_handmade_package_09():
    r'''Make handmade package. Copy canned material definition module. 
    Make output data. Corrupt output data. Verify invalid output material 
    module. Remove package.
    '''

    score_manager = scoremanager.core.ScoreManager()
    name = 'scoremanager.materialpackages.testnotes'
    assert not score_manager.configuration.package_path_exists(name)

    try:
        score_manager._run(pending_user_input=
            'lmm nmh testnotes default default '
            'testnotes mdcanned boilerplate_testnotes_material_definition.py default '
            'omm default '
            'omcanned boilerplate_exception.py default q')
        assert score_manager.configuration.package_path_exists(name)
        mpp = scoremanager.managers.MaterialPackageManager(name)
        assert mpp._list_directory() == [
            '__init__.py',
            '__metadata__.py',
            'illustration_builder.py', 
            'material_definition.py', 
            'output_material.py', 
            ]
        assert mpp.has_illustration_builder_module
        assert mpp.material_definition and \
            all(isinstance(x, Note) for x in mpp.material_definition)
        assert mpp.output_material is None
    finally:
        string = 'lmm testnotes del remove default q'
        score_manager._run(pending_user_input=string)
        assert not score_manager.configuration.package_path_exists(name)


def test_MaterialPackageWrangler_run_handmade_package_10():
    r'''Make handmade package. Copy canned material definition module.
    Make output data. Make PDF. Remove package.
    '''
    pytest.skip(
        'skip this one during day-to-day development and before build only.')

    score_manager = scoremanager.core.ScoreManager()
    name = 'scoremanager.materialpackages.testnotes'
    assert not score_manager.configuration.package_path_exists(name)

    try:
        score_manager._run(pending_user_input=
            'lmm nmh testnotes default default '
            'testnotes mdcanned boilerplate_testnotes_material_definition.py default '
            'omm default '
            'pdfm default '
            'q')
        assert score_manager.configuration.package_path_exists(name)
        mpp = scoremanager.managers.MaterialPackageManager(name)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'illustration.ly', 
            'illustration.pdf',
            'illustration_builder.py', 
            'material_definition.py', 
            'output_material.py', 
            ]
        assert mpp.has_illustration_ly
        assert mpp.has_illustration_pdf
        assert mpp.material_definition and \
            all(isinstance(x, Note) for x in mpp.material_definition)
        assert mpp.output_material and \
            all(isinstance(x, Note) for x in mpp.output_material)
            
    finally:
        string = 'lmm testnotes del remove default q'
        score_manager._run(pending_user_input=string)
        assert not score_manager.configuration.package_path_exists(name)
