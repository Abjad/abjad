# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
from experimental import *
import scoremanager


def test_ArticulationHandlerMaterialManager_01():

    score_manager = scoremanager.core.ScoreManager()
    configuration = score_manager._configuration
    path = os.path.join(
        configuration.abjad_material_packages_directory_path,
        'testarticulationhandler',
        )
    assert not os.path.exists(path)
    directory_entries = [
        '__init__.py', 
        '__metadata__.py',
        'output_material.py', 
        ]
    handler = handlertools.ReiteratedArticulationHandler(
        articulation_list=['^', '.'],
        minimum_duration=Duration(1, 64),
        maximum_duration=Duration(1, 4),
        minimum_written_pitch=NamedPitch('c'),
        maximum_written_pitch=NamedPitch("c''''"),
        )
    input_ = 'lmm nmm articulation testarticulationhandler default'
    input_ += ' reiterated'
    input_ += " ['^', '.'] (1, 64) (1, 4) c c'''' done default"
    input_ += ' q'

    try:
        score_manager._run(pending_user_input=input_, is_test=True)
        assert os.path.exists(path)
        manager = scoremanager.managers.ArticulationHandlerMaterialManager
        manager = manager(path=path)
        assert manager._list() == directory_entries
        output_material = manager._execute_output_material_module()
        assert output_material == handler
        input_ = 'lmm testarticulationhandler rm remove q'
        score_manager._run(pending_user_input=input_, is_test=True)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)

    assert not os.path.exists(path)
