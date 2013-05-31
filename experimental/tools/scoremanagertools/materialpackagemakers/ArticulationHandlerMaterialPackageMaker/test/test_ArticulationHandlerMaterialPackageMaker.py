from experimental import *


def test_ArticulationHandlerMaterialPackageMaker_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not score_manager.configuration.packagesystem_path_exists(
        'experimental.tools.scoremanagertools.materialpackages.testarticulationhandler')
    try:
        score_manager._run(user_input=
            'materials maker articulation testarticulationhandler default '
            'testarticulationhandler omi reiterated '
            "['^', '.'] (1, 64) (1, 4) c c'''' done default "
            'q '
            )
        mpp = scoremanagertools.materialpackagemakers.ArticulationHandlerMaterialPackageMaker(
            'experimental.tools.scoremanagertools.materialpackages.testarticulationhandler')
        assert mpp.list_directory() == ['__init__.py', 'output_material.py', 'tags.py']
        handler = handlertools.ReiteratedArticulationHandler(
            articulation_list=['^', '.'],
            minimum_duration=Duration(1, 64),
            maximum_duration=Duration(1, 4),
            minimum_written_pitch=pitchtools.NamedChromaticPitch('c'),
            maximum_written_pitch=pitchtools.NamedChromaticPitch("c''''"),
            )
        assert mpp.output_material == handler
    finally:
        score_manager._run(user_input='m testarticulationhandler del remove default q')
        assert not score_manager.configuration.packagesystem_path_exists(
            'experimental.tools.scoremanagertools.materialpackages.testarticulationhandler')
