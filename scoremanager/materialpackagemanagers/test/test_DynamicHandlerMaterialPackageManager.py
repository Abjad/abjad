# -*- encoding: utf-8 -*-
from abjad import *
from experimental import *
import scoremanager


def test_DynamicHandlerMaterialPackageManager_01():

    score_manager = scoremanager.core.ScoreManager()
    string = 'scoremanager.materialpackages.testdynamichandler'
    assert not score_manager.configuration.package_exists(string)
    try:
        score_manager._run(pending_user_input=
            'lmm nmm dynamic testdynamichandler default '
            'testdynamichandler omi reiterateddynamic '
            'f (1, 16) done default '
            'q '
            )
        string = 'scoremanager.materialpackages.testdynamichandler'
        mpp = scoremanager.materialpackagemanagers.DynamicHandlerMaterialPackageManager(
            string)
        assert mpp._list_directory() == [
            '__init__.py', 
            '__metadata__.py',
            'illustration_builder.py',
            'output_material.py', 
            ]
        handler = handlertools.ReiteratedDynamicHandler(
            dynamic_name='f',
            minimum_duration=Duration(1, 16),
            )
        assert mpp.output_material == handler
    finally:
        string = 'lmm testdynamichandler del remove default q'
        score_manager._run(pending_user_input=string)
        string = 'scoremanager.materialpackages.testdynamichandler'
        assert not \
            score_manager.configuration.package_exists(string)
