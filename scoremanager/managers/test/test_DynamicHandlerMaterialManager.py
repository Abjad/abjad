# -*- encoding: utf-8 -*-
import os
from abjad import *
from experimental import *
import scoremanager


def test_DynamicHandlerMaterialManager_01():

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.abjad_material_packages_directory_path,
        'testdynamichandler',
        )
    assert not os.path.exists(path)
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'output_material.py', 
        ]
    handler = handlertools.ReiteratedDynamicHandler(
        dynamic_name='f',
        minimum_duration=Duration(1, 16),
        )
    input_ = 'lmm nmm dynamic testdynamichandler default'
    input_ += ' reiterateddynamic f (1, 16) done default q'

    try:
        score_manager._run(pending_user_input=input_)
        manager = scoremanager.managers.DynamicHandlerMaterialManager(
            path=path)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_material_module()
        assert output_material == handler
    finally:
        string = 'lmm testdynamichandler rm remove q'
        score_manager._run(pending_user_input=string)
        assert not os.path.exists(path)
