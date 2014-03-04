# -*- encoding: utf-8 -*-
import os
from abjad import *
from experimental import *
import scoremanager


def test_DynamicHandlerMaterialManager_01():

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    string = 'scoremanager.materials.testdynamichandler'
    assert not score_manager._configuration.package_exists(string)
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'output_material.py', 
        ]
    handler = handlertools.ReiteratedDynamicHandler(
        dynamic_name='f',
        minimum_duration=Duration(1, 16),
        )

    try:
        score_manager._run(pending_user_input=
            'lmm nmm dynamic testdynamichandler default '
            'testdynamichandler omi reiterateddynamic '
            'f (1, 16) done default '
            'q '
            )
        path = configuration.abjad_material_packages_directory_path
        path = os.path.join(path, 'testdynamichandler')
        manager = scoremanager.managers.DynamicHandlerMaterialManager(
            path=path)
        assert manager._list_directory() == directory_entries
        output_material = manager._execute_output_material_module()
        assert output_material == handler
    finally:
        string = 'lmm testdynamichandler rm remove q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materials.testdynamichandler'
        assert not score_manager._configuration.package_exists(string)
