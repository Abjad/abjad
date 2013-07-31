# -*- encoding: utf-8 -*-
from experimental import *


def test_DynamicHandlerMaterialPackageMaker_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'experimental.tools.scoremanagertools.materialpackages.testdynamichandler')
    try:
        score_manager._run(pending_user_input=
            'materials maker dynamic testdynamichandler default '
            'testdynamichandler omi reiterateddynamic '
            'f (1, 16) done default '
            'q '
            )
        mpp = scoremanagertools.materialpackagemakers.DynamicHandlerMaterialPackageMaker(
            'experimental.tools.scoremanagertools.materialpackages.testdynamichandler')
        assert mpp.list_directory() == ['__init__.py', 'output_material.py', 'tags.py']
        handler = handlertools.ReiteratedDynamicHandler(
            dynamic_name='f',
            minimum_duration=Duration(1, 16),
            )
        assert mpp.output_material == handler
    finally:
        score_manager._run(pending_user_input='m testdynamichandler del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'experimental.tools.scoremanagertools.materialpackages.testdynamichandler')
