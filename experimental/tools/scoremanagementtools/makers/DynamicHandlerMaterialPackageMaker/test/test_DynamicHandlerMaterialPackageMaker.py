from abjad import *
from experimental.tools import handlertools
from experimental import *


def test_DynamicHandlerMaterialPackageMaker_01():

    studio = scoremanagementtools.studio.ScoreManager()
    assert not studio.package_exists('materials.testdynamichandler')
    try:
        studio.run(user_input=
            'materials maker dynamic testdynamichandler default '
            'testdynamichandler omi reiterateddynamic '
            'f (1, 16) done default '
            'q '
            )
        mpp = scoremanagementtools.makers.DynamicHandlerMaterialPackageMaker('materials.testdynamichandler')
        assert mpp.directory_contents == ['__init__.py', 'output_material.py', 'tags.py']
        handler = handlertools.ReiteratedDynamicHandler(
            dynamic_name='f',
            minimum_duration=Duration(1, 16),
            )
        assert mpp.output_material == handler
    finally:
        studio.run(user_input='m testdynamichandler del remove default q')
        assert not studio.package_exists('materials.testdynamichandler')
