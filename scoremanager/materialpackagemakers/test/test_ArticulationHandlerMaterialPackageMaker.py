# -*- encoding: utf-8 -*-
from experimental import *


def test_ArticulationHandlerMaterialPackageMaker_01():

    score_manager = scoremanager.core.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'scoremanager.materialpackages.testarticulationhandler')
    try:
        score_manager._run(pending_user_input=
            'materials maker articulation testarticulationhandler default '
            'testarticulationhandler omi reiterated '
            "['^', '.'] (1, 64) (1, 4) c c'''' done default "
            'q '
            )
        mpp = scoremanager.materialpackagemakers.ArticulationHandlerMaterialPackageMaker(
            'scoremanager.materialpackages.testarticulationhandler')
        assert mpp._list_directory() == [
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
        assert mpp.output_material == handler
    finally:
        score_manager._run(pending_user_input='m testarticulationhandler del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'scoremanager.materialpackages.testarticulationhandler')
