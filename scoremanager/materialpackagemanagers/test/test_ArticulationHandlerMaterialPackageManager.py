# -*- encoding: utf-8 -*-
from abjad import *
from experimental import *
import scoremanager


def test_ArticulationHandlerMaterialPackageManager_01():

    score_manager = scoremanager.core.ScoreManager()
    string = 'scoremanager.materialpackages.testarticulationhandler'
    assert not score_manager.configuration.packagesystem_path_exists(string)
    try:
        score_manager._run(pending_user_input=
            'materials nmm articulation testarticulationhandler default '
            'testarticulationhandler omi reiterated '
            "['^', '.'] (1, 64) (1, 4) c c'''' done default "
            'q '
            )
        string = 'scoremanager.materialpackages.testarticulationhandler'
        manager = scoremanager.materialpackagemanagers.ArticulationHandlerMaterialPackageManager(
            string)
        assert manager._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'illustration_builder.py',
            'output_material.py', 
            ]
        handler = handlertools.ReiteratedArticulationHandler(
            articulation_list=['^', '.'],
            minimum_duration=Duration(1, 64),
            maximum_duration=Duration(1, 4),
            minimum_written_pitch=NamedPitch('c'),
            maximum_written_pitch=NamedPitch("c''''"),
            )
        assert manager.output_material == handler
    finally:
        string = 'mlm testarticulationhandler del remove default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materialpackages.testarticulationhandler'
        assert not \
            score_manager.configuration.packagesystem_path_exists(string)
