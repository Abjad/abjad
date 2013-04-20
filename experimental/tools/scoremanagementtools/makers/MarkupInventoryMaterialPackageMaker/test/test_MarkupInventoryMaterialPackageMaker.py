from abjad import *
from experimental import *


def test_MarkupInventoryMaterialPackageMaker_01():

    studio = scoremanagementtools.studio.ScoreManager()
    assert not studio.package_exists('materials.testmarkupinventory')
    try:
        studio.run(user_input=
            "materials maker markup testmarkupinventory "
            "omi name test~markup~inventory "
            "add arg r'\\italic~{~serenamente~}' name serenamente done "
            "add arg r'\\italic~{~presto~}' name presto done done default q"
            )
        mpp = scoremanagementtools.makers.ArticulationHandlerMaterialPackageMaker('materials.testmarkupinventory')
        assert mpp.directory_contents == ['__init__.py', 'output_material.py', 'tags.py']
        inventory = markuptools.MarkupInventory([
            markuptools.Markup(
                '\\italic { serenamente }',
                markup_name='serenamente'
                ),
            markuptools.Markup(
                '\\italic { presto }',
                markup_name='presto'
                )
            ],
            name='test markup inventory'
            )
        assert mpp.output_material == inventory
    finally:
        studio.run(user_input='m testmarkupinventory del remove default q')
        assert not studio.package_exists('materials.testmarkupinventory')
