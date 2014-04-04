# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
from experimental import *
import scoremanager


def test_DynamicHandlerMaterialManager_edit_output_material_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.user_library_material_packages_directory_path,
        'testdynamichandler',
        )
    assert not os.path.exists(path)
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'output.py',
        ]
    handler = handlertools.ReiteratedDynamicHandler(
        dynamic_name='f',
        minimum_duration=Duration(1, 16),
        )
    input_ = 'm nmm dynamic testdynamichandler default'
    input_ += ' reiterateddynamic f (1, 16) done default q'

    try:
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.DynamicHandlerMaterialManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_module()
        assert output_material == handler
        input_ = 'm testdynamichandler rm remove q'
        score_manager._run(pending_user_input=input_)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)

    assert not os.path.exists(path)