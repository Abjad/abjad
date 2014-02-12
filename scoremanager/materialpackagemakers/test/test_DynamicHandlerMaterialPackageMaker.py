# -*- encoding: utf-8 -*-
from abjad import *
from experimental import *
import scoremanager


def test_DynamicHandlerMaterialPackageMaker_01():

    score_manager = scoremanager.core.ScoreManager()
    string = 'scoremanager.materialpackages.testdynamichandler'
    assert not score_manager.configuration.packagesystem_path_exists(string)
    try:
        score_manager._run(pending_user_input=
            'materials maker dynamic testdynamichandler default '
            'testdynamichandler omi reiterateddynamic '
            'f (1, 16) done default '
            'q '
            )
        string = 'scoremanager.materialpackages.testdynamichandler'
        mpp = scoremanager.materialpackagemakers.DynamicHandlerMaterialPackageMaker(
            string)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'output_material.py', 
            ]
        handler = handlertools.ReiteratedDynamicHandler(
            dynamic_name='f',
            minimum_duration=Duration(1, 16),
            )
        assert mpp.output_material == handler
    finally:
        string = 'm testdynamichandler del remove default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materialpackages.testdynamichandler'
        assert not \
            score_manager.configuration.packagesystem_path_exists(string)
