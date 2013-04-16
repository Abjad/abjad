from abjad import *
from experimental.tools import handlertools
from experimental import *


def test_ArticulationHandlerMaterialPackageMaker_01():

    studio = scoremanagementtools.studio.Studio()
    assert not studio.package_exists('materials.testarticulationhandler')
    try:
        studio.run(user_input=
            'materials maker articulation testarticulationhandler default '
            'testarticulationhandler omi reiterated '
            "['^', '.'] (1, 64) (1, 4) c c'''' done default "
            'q '
            )
        mpp = scoremanagementtools.makers.ArticulationHandlerMaterialPackageMaker('materials.testarticulationhandler')
        assert mpp.directory_contents == ['__init__.py', 'output_material.py', 'tags.py']
        handler = handlertools.ReiteratedArticulationHandler(
            articulation_list=['^', '.'],
            minimum_duration=Duration(1, 64),
            maximum_duration=Duration(1, 4),
            minimum_written_pitch=pitchtools.NamedChromaticPitch('c'),
            maximum_written_pitch=pitchtools.NamedChromaticPitch("c''''"),
            )
        assert mpp.output_material == handler
    finally:
        studio.run(user_input='m testarticulationhandler del remove default q')
        assert not studio.package_exists('materials.testarticulationhandler')
