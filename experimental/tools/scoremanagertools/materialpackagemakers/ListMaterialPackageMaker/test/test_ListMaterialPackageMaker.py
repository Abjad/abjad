from experimental import *


def test_ListMaterialPackageMaker_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not packagepathtools.package_exists('system_materials.testlist')
    try:
        score_manager._run(user_input=
            'materials maker list testlist '
            "17 foo done b default q "
            )
        mpp = scoremanagertools.materialpackagemakers.ListMaterialPackageMaker('system_materials.testlist')
        assert mpp.list_directory() == ['__init__.py', 'output_material.py', 'tags.py']
        assert mpp.output_material == [17, 'foo']
    finally:
        score_manager._run(user_input='m testlist del remove default q')
        assert not packagepathtools.package_exists('system_materials.testlist')
